"""Basic webapp to display top news stories with NewsAPI"""

from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from newsapi import NewsApiClient


# Initialize Flask, newsapi and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
newsapi = NewsApiClient(api_key = '85dd624eda284c998d1b3ba8ac0bb600')


class Story(db.Model):
    """Database object to store retrieved stories."""
    id = db.Column(db.Integer, primary_key=True)
    source_name = db.Column(db.String(100))
    author = db.Column(db.String(100))
    title = db.Column(db.String(100))
    url = db.Column(db.String(100))
    image_url = db.Column(db.String(100))
    published_at = db.Column(db.String(100))

    def __repr__(self):
        return '<Story %r>' % self.id


@app.route('/')
def index():
    """Display homepage"""
    # Automatically update if database is empty
    if db.session.query(Story).count() == 0:
        return redirect('/update/')

    # Display stories stored in database
    stories = Story.query.order_by(Story.title).all()
    return render_template('index.html', stories=stories)



@app.route('/update/')
def refresh_stories():
    """Replace existing stories in DB, if any, with new ones"""

    # Delete old stories if needed
    if db.session.query(Story).count() > 0:
        db.session.query(Story).delete()
        db.session.commit()

    # Get new stories from NewsAPI
    stories = newsapi.get_top_headlines()
    print("got " + str(len(stories['articles'])) + " stories")

    # Turn each story into an SQLalchemy Story object
    for story in stories['articles']:
        db_model = Story(
            source_name=story["source"]["name"],
            author=story["author"], 
            title=story["title"],
            url=story["url"],
            image_url=story["urlToImage"], 
            published_at=story["publishedAt"])
        db.session.add(db_model)
    
    # Commit db changes and redirect to home page
    db.session.commit()
    print("Stories updated successfully")
    return redirect('/')

if __name__ == "__main__":
    """Run dev server"""
    app.run(debug=True)