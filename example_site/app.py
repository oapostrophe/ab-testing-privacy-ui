"""Basic webapp to display top news stories with NewsAPI"""

from flask import Flask, render_template, redirect, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from newsapi import NewsApiClient
import time, hashlib
from userdata import Event

# Initialize Flask, newsapi and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
newsapi = NewsApiClient(api_key = '85dd624eda284c998d1b3ba8ac0bb600')

# Load time stories were last updated from file
try:
    with open('last_updated.txt', "r") as file:
        time_string = file.read()
        file.close()
        last_updated = int(float(time_string))

except:
    last_updated = 0

# Initialize array for logging page visit data in memory
events = []

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
        return "<Story %r>" % self.id


@app.route('/', methods=['GET', 'POST'])
def index():
    """Display homepage, and log user events"""

    # Log data from POST request upon user click
    if request.method == "POST":
        timestamp = time.time()
        event_type = str(request.data)[2:-1]
        log_event(events, request, timestamp, event_type)
        response = make_response(jsonify({"message" : "event logged"}), 200)
        return response
    
    # Display home page and log user opening page
    else:
        timestamp = time.time()
        log_event(events, request, timestamp, "page_open")
        stories = get_stories()
        return render_template('index.html', stories=stories, 
                                title="Trending Stories")

def log_event(events, request, timestamp, event_type):
    """Log interaction during page visit received through POST request
    
    :param events: (list) Current events list in memory, to be appended
    :param timestamp: (int) Request timestamp as Unix int
    :param request: Flask request object
    """
    # Get IP and convert to string
    ip = str(request.remote_addr)[2:-1]
    ip = ip.encode()

    # Hash IP into user ID
    user_id = hashlib.sha256(ip).hexdigest()

    # Get element_id if event is a click
    if event_type == "click":
        element_id = str(request.data)[2:-1]
    else:
        element_id = None

    # Add to events log
    events.append(Event(user_id, timestamp, event_type, element_id))


@app.route('/international/')
def international():
    """Display international sources"""
    stories = get_stories(sources = ["BBC News", "Reuters", "Al Jazeera English"])
    return render_template('index.html', stories=stories,
                             title="International Coverage")

def get_stories(sources=None):
    """Get stories from specified sources.

    :param stories: (array) Array of strings containing Story.source_name 
    values by which to filter database. Default value None will display all
    stories.
    """

    # Automatically update database if needed
    if db.session.query(Story).count() == 0 \
        or int(time.time()) - last_updated > 3600:
        refresh_stories()
    
    # Display all stories if given default sources value
    if sources == None:
         return Story.query.all()
    
    # Display stories from specified sources
    stories = []
    for source in sources:
        source_stories = Story.query.filter_by(source_name=source).all()
        stories.extend(source_stories)
    return stories


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

    # Commit database changes
    db.session.commit()


def refresh_stories():
    """Put new stories in database"""

    # Delete any old stories in database
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

    # Record time updated
    global last_updated
    last_updated = int(time.time())
    with open("last_updated.txt", "w") as file:
        file.write(str(last_updated))
        file.close()

if __name__ == "__main__":
    """Run dev server"""

    # Run server
    app.run(debug=True)

    # Store current session id
    with open("next_session_id.txt", "w") as file:
        file.write(str(next_session_id))
        file.close()