"""Basic webapp to display top news stories with NewsAPI"""

from flask import Flask, render_template, redirect, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from newsapi import NewsApiClient
import time, hashlib, json, csv
from userdata import Event


# Initialize Flask, newsapi and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
newsapi = NewsApiClient(api_key = '85dd624eda284c998d1b3ba8ac0bb600')

# Load last time stories were updated from file
try:
    with open('last_updated.txt', "r") as file:
        time_string = file.read()
        file.close()
        last_updated = int(float(time_string))

except:
    last_updated = 0

# Initialize array for logging page data in memory
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


def log_event(events, request, timestamp, event_type, element_id=None):
    """Log page events such as opening, closing, and clicks
    
    :param events: (list) Current events list in memory, to be appended
    :param request: Flask request object
    :param timestamp: (int) Request timestamp as Unix int
    :param event_type: (str) "page_open", "click", or "page_close"
    :param element_id: (str) optional identifier for clicks of which page
    element was clicked on.
    """
    # Get IP and convert to string
    ip = str(request.remote_addr)[2:-1]
    ip = ip.encode()

    # Hash IP into user ID
    user_id = hashlib.sha256(ip).hexdigest()

    # Add to events log
    events.append(Event(user_id, timestamp, request.url, event_type,
                     element_id))


def get_stories(sources=None):
    """Get stories from specified sources.

    :param sources: (list) List of strings containing Story.source_name 
    values by which to filter database. Default value None will display all
    stories.
    """

    # Automatically update database if needed
    if db.session.query(Story).count() == 0 \
        or (time.time() - last_updated) > 3600:
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
    
    # Refresh time last updated
    global last_updated
    last_updated = time.time()
    print("last updated now updated to:")
    print(last_updated)
    with open("last_updated.txt", "w") as file:
        file.write(str(last_updated))
        file.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    """Display homepage.  GET request will be sent upon opening page and will
        always log a page_open event.  POST request will be sent when the page
        closes, or when the user clicks on certain page elements, and will
        contain the event type and, if a click, the id of the element 
        clicked on."""

    # Log data from POST request upon user click
    if request.method == "POST":
        data = request.get_json()
        log_event(events, request, data["timestamp"], data["event_type"], 
                    data["element_id"])
        return make_response(jsonify({"message":"ok"}), 200)
    
    # Display home page and log user opening page
    else:
        stories = get_stories()
        return render_template('index.html', stories=stories)


@app.route('/left/', methods = ['GET', 'POST'])
def left():
    """Display left-leaning sources and log page events, following protocol
        documented in homepage "/" route."""

    # Log data from POST request upon user click
    if request.method == "POST":
        data = request.get_json()
        log_event(events, request, data["timestamp"], data["event_type"], 
                    data["element_id"])
        return make_response(jsonify({"message":"ok"}), 200)
    
    # Display page and log user opening page
    else:
        stories = get_stories(sources = ["Vice News", "The Washington Post"])
        return render_template('left.html', stories=stories)


@app.route('/center/', methods = ['GET', 'POST'])
def center():
    """Display cener-leaning sources and log page events, following protocol
        documented in homepage "/" route."""

     # Log data from POST request upon user click
    if request.method == "POST":
        data = request.get_json()
        log_event(events, request, data["timestamp"], data["event_type"], 
                    data["element_id"])
        return make_response(jsonify({"message":"ok"}), 200)
    
    # Display page and log user opening page
    else:
        stories = get_stories(sources = ["USA Today", "CNN"])
        return render_template('center.html', stories=stories)


@app.route('/right/', methods = ['GET', 'POST'])
def right():
    """Display right-leaning sources and log page events, following protocol
        documented in homepage "/" route."""

     # Log data from POST request upon user click
    if request.method == "POST":
        data = request.get_json()
        log_event(events, request, data["timestamp"], data["event_type"], 
                    data["element_id"])
        return make_response(jsonify({"message":"ok"}), 200)
    
    # Display page and log user opening page
    else:
        stories = get_stories(sources = ["Breitbart News", "The Washington Times"])
        return render_template('right.html', stories=stories)


@app.route('/international/', methods = ['GET', 'POST'])
def international():
    """Display right-leaning sources and log page events, following protocol
        documented in homepage "/" route."""

     # Log data from POST request upon user click
    if request.method == "POST":
        data = request.get_json()
        log_event(events, request, data["timestamp"], data["event_type"], 
                    data["element_id"])
        return make_response(jsonify({"message":"ok"}), 200)
    
    # Display page and log user opening page
    else:
        stories = get_stories(sources = ["BBC News", "Reuters", "Al Jazeera English"])
        return render_template('international.html', stories=stories)


if __name__ == "__main__":
    """Run dev server and log data to csv after server closes."""

    # Run Flask server
    app.run(debug=True)
    
    # Check if csv file already exists
    try:
        file = open("data_log.csv", "r")
        file.close()

    # Create csv file if not present
    except:
        file = open("data_log.csv", "w", newline = '')
        heading_writer = csv.writer(file, delimiter=',', quotechar='"',
                                    quoting = csv.QUOTE_ALL)
        heading_writer.writerow(['user_id', 'timestamp', 'url', 'event_type',
                                 'element_id'])
        file.close()

    # Write data from events list to csv file
    with open("data_log.csv", "a", newline='') as file:
        writer = csv.writer(file, delimiter = ',', quotechar = '"',
                    quoting = csv.QUOTE_ALL)
        for event in events:
            row = [event.user_id, event.timestamp, event.url, event.event_type,
                    event.element_id]
            writer.writerow(row)
        file.close()
