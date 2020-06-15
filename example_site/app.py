"""Basic webapp to display top news stories with NewsAPI"""

from flask import Flask, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from newsapi import NewsApiClient
from flask_migrate import Migrate

# Initialize Flask, newsapi and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
newsapi = NewsApiClient(api_key = '85dd624eda284c998d1b3ba8ac0bb600')
migrate = Migrate(app, db)

class Story(db.Model):
    """Database object to store retrieved stories."""
    id = db.Column(db.Integer, primary_key=True)
    source_name = db.Column(db.String(100))
    author = db.Column(db.String(100))
    title = db.Column(db.String(100))
    url = db.Column(db.String(100))
    image_url = db.Column(db.String(100))
    published_at = db.Column(db.String(100))
    description = db.Column(db.String(200))

    def __repr__(self):
        return '<Story %r>' % self.id


@app.route('/')
def index():
    """Display homepage"""
    # Automatically update if database is empty
    if db.session.query(Story).count() == 0:
        return redirect('/update/')

    # Display stories stored in database
    stories = Story.query.all()
    for story in stories:
        print(story.description)
    return render_template('index.html', stories=stories)

def add_stories(source, max_stories):
    """Get stories from specified NewsAPI source.  Convert into SQLalchemy 
    ojects and add to specified limit of stories to database.

    :param source: (str) "sources" argument for newsapi.
    :param max_stories: (int) Maximum number of stories to store.
    """

    # Get stories from NewsAPI as dict
    stories = newsapi.get_top_headlines(sources=source)

    # Convert to SQLalchemy object and add to database, up to max_stories times
    count = 0
    for story in stories['articles']:
        if count < max_stories:

            # Convert to SQLalchemy object
            db_model = Story(
                source_name=story["source"]["name"],
                author=story["author"], 
                title=story["title"],
                url=story["url"],
                image_url=story["urlToImage"], 
                published_at=story["publishedAt"],
                description=story["description"])
            db.session.add(db_model) # Add to database
        count += 1
    db.session.commit() # Commit database changes

@app.route('/update/')
def refresh_stories():
    """Put new stories in database"""

    # Delete old stories in database if needed
    if db.session.query(Story).count() > 0:
        db.session.query(Story).delete()
        db.session.commit()

    # Add 5 stories from each NewsAPI source
    add_stories('vice-news', 3)
    add_stories('the-washington-post', 3)
    add_stories('usa-today', 3)
    add_stories('cnn', 3)
    add_stories('the-washington-times', 3)
    add_stories('breitbart-news', 3)
    add_stories('al-jazeera-english', 3)
    add_stories('bbc-news', 3)
    add_stories('reuters', 3)

    # Redirect to homepage
    return redirect('/')

if __name__ == "__main__":
    """Run dev server"""
    app.run(debug=True)