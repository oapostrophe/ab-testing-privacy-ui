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
    """Database object to store retrieved stories.

    id: Integer serving as primary identifier
    source_name: String identifying source that published the article
    author: Author's name
    title: Title/Headline of article
    url: Link to article on original source site
    published_at: String with date/time published
    description: First 200 characters of the article.
    """
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


def log_event(events, request):
    """Log page events such as opening, closing, and clicks
    
    :param events: (list) Current events list, appends event here.
    :param request: Flask request object
    """
    # Get IP and convert to string
    user_id = str(request.remote_addr)[2:-1]
    user_id = user_id.encode()

    # Hash IP into user ID
    user_id = hashlib.sha256(user_id).hexdigest()

    # Cast data to string into separate elements
    datalist = str(request.data)[2:-1].split(';')

    # Add to events log
    events.append(Event(user_id, datalist[0], request.url, datalist[1],
                     datalist[2]))


def get_stories(sources=None):
    """Returns stories from a list of sources.

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
    """Add stories from specified NewsAPI source to database, up to given
    limit on number of stories.

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
    """Update database of stories from NewsAPI."""

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
    """ Display homepage.  GET request displays page, POST requests are sent to
    log a page event: page_load, page_focus, page_blur, or clicks.
    """

    # Log data from POST request
    if request.method == "POST":
        log_event(events, request)
        return make_response(jsonify({"message":"ok"}), 200)
        
    # Display home page upon GET request
    else:
        stories = get_stories()
        return render_template('index.html', stories=stories)


@app.route('/left/', methods = ['GET', 'POST'])
def left():
    """Display left-leaning sources and log page events from POST requests."""

    # Log data from POST request
    if request.method == "POST":
        log_event(events, request)
        return make_response(jsonify({"message":"ok"}), 200)
    
    # Display page
    else:
        stories = get_stories(sources = ["Vice News", "The Washington Post"])
        return render_template('left.html', stories=stories)


@app.route('/center/', methods = ['GET', 'POST'])
def center():
    """Display cener-leaning sources and log page events from POST requests."""

     # Log data from POST request
    if request.method == "POST":
        log_event(events, request)
        return make_response(jsonify({"message":"ok"}), 200)
    
    # Display page
    else:
        stories = get_stories(sources = ["USA Today", "CNN"])
        return render_template('center.html', stories=stories)


@app.route('/right/', methods = ['GET', 'POST'])
def right():
    """Display right-leaning sources and log page events from POST requests."""

     # Log data from POST request
    if request.method == "POST":
        log_event(events, request)
        return make_response(jsonify({"message":"ok"}), 200)
    
    # Display page
    else:
        stories = get_stories(sources = ["Breitbart News", "The Washington Times"])
        return render_template('right.html', stories=stories)


@app.route('/international/', methods = ['GET', 'POST'])
def international():
    """Display right-leaning sources and log page events from POST requests."""

     # Log data from POST request
    if request.method == "POST":
        log_event(events, request)
        return make_response(jsonify({"message":"ok"}), 200)
    
    # Display page
    else:
        stories = get_stories(sources = ["BBC News", "Reuters", "Al Jazeera English"])
        return render_template('international.html', stories=stories)


if __name__ == "__main__":
    """Run dev server and log data to csv after server closes."""

    # Run Flask server
    app.run(debug=True, host="192.168.1.239")
    
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