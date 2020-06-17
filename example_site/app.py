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
    description = db.Column(db.String(200))

    def __repr__(self):
        return '<Story %r>' % self.id


@app.route('/')
def index():
    """Display homepage"""
    # Automatically update if database is empty
    if db.session.query(Story).count() == 0:
        refresh_stories()

    # Display stories stored in database
    stories = Story.query.all()
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
            print("headline:")
            print(db_model.title)
            print("description:")
            print(db_model.description)
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

    # Add 3 stories from each NewsAPI source
    add_stories('vice-news', 3)
    add_stories('the-washington-post', 3)
    add_stories('usa-today', 3)
    add_stories('cnn', 3)
    add_stories('the-washington-times', 3)
    add_stories('breitbart-news', 3)
    add_stories('al-jazeera-english', 3)
    add_stories('bbc-news', 3)
    add_stories('reuters', 3)

    print("Successfully updated!")

    # Redirect to homepage
    return redirect('/')
@app.route('/cnn/')
def cnn_index():
    if db.session.query(Story).count() == 0:
        return redirect('/update/')
    stories = Story.query.filter_by(source_name='CNN').all()
    return render_template('cnn.html', stories=stories)

def add_cnn_stories(source, max_stories):
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
                published_at=story["publishedAt"])
            db.session.add(db_model) # Add to database
        count += 1

    db.session.commit() # Commit database changes

@app.route('/vice/')
def vice_index():
    if db.session.query(Story).count() == 0:
        return redirect('/update/')
    stories = Story.query.filter_by(source_name='Vice News').all()
    return render_template('vice.html', stories=stories)

def add_vice_stories(source, max_stories):
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
                published_at=story["publishedAt"])
            db.session.add(db_model) # Add to database
        count += 1

    db.session.commit() # Commit database changes

@app.route('/washingtonpost/')
def wp_index():
    if db.session.query(Story).count() == 0:
        return redirect('/update/')
    stories = Story.query.filter_by(source_name='The Washington Post').all()
    return render_template('washingtonpost.html', stories=stories)

def add_wp_stories(source, max_stories):
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
                published_at=story["publishedAt"])
            db.session.add(db_model) # Add to database
        count += 1

    db.session.commit() # Commit database changes

@app.route('/usatoday/')
def usatoday_index():
    if db.session.query(Story).count() == 0:
        return redirect('/update/')
    stories = Story.query.filter_by(source_name='USA Today').all()
    return render_template('usatoday.html', stories=stories)

def add_usatoday_stories(source, max_stories):
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
                published_at=story["publishedAt"])
            db.session.add(db_model) # Add to database
        count += 1

    db.session.commit() # Commit database changes
if __name__ == "__main__":
    """Run dev server"""
    app.run(debug=True)