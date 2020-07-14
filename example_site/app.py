"""Basic webapp to display top news stories with NewsAPI"""

from flask import Flask, render_template, redirect, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from newsapi import NewsApiClient
import time, hashlib, json, csv, random
from userdata import Event


# Initialize Flask, newsapi and SQLalchemy
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


def log_event(request, get=False):
    """Log page events such as opening, closing, and clicks
    
    :param request: Flask request object
    :param get: (bool) True if request isa  GET, false if POST.  Should only be
    true when logging the initial visit that has an Mturk survey id, all other
    events will be through POST requests.
    """

    # Get IP and convert to string
    user_id = str(request.remote_addr)[2:-1]
    user_id = user_id.encode()

    # Hash IP into user ID
    user_id = hashlib.sha256(user_id).hexdigest()

    # Log data to console if POST request
    if get == False:
        data = str(request.data)[2:-1].split(';;;')
        log = [user_id, request.url.split("?")[0], data[0], data[1], data[2], data[3], data[4],
                data[5]]
        print('"'+log[0]+'",'+'"'+log[1]+'",'+'"'+log[2]+'",'+'"'+log[3]+'",'+
              '"'+log[4]+'",'+'"'+log[5]+'",'+'"'+log[6]+'",'+'"'+log[7]+'",')

    # Log event to link survey ID on GET request
    else:
        log = [user_id, request.url.split("?")[0], str(round(time.time(), 1)), "survey_id", 
                request.args["id"], "nobanner", "na", "na"]
        print('"'+log[0]+'",'+'"'+log[1]+'",'+'"'+log[2]+'",'+'"'+log[3]+'",'+
              '"'+log[4]+'",'+'"'+log[5]+'",'+'"'+log[6]+'",'+'"'+log[7]+'",')


def get_stories(sources=None):
    """Returns stories from a list of sources.

    :param sources: (list) List of strings containing Story.source_name 
    values by which to filter database. Default value None will display all
    stories.
    """

    # Automatically update database if needed
    if db.session.query(Story).count() == 0 \
        or (time.time() - last_updated) > 43200:
        refresh_stories()

    # Return all stories in database if given default sources value
    if sources == None:
         stories = Story.query.all()
         random.shuffle(stories)
         return stories
    
    # Return stories from specified sources
    stories = []
    for source in sources:
        source_stories = Story.query.filter_by(source_name=source).all()
        stories.extend(source_stories)
    random.shuffle(stories)
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
    add_stories('the-huffington-post', 3)
    add_stories('politico', 3)
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
    with open("last_updated.txt", "w") as file:
        file.write(str(last_updated))
        file.close()


@app.route('/', methods=['GET', 'POST'])
def index():
    """ Display homepage.  GET request displays page, POST requests are sent to
    log page events.
    """

    # Log data from POST requests
    if request.method == "POST":
        log_event(request)
        return make_response(jsonify({"message":"ok"}), 200)
        
    # Display page for GET requests
    else:
        # Log survey id if present
        try:
            log_event(request, True)
        except:
            pass

        # Determine CCPA banner configuration based on user IP
        user_id = str(request.remote_addr)[2:-1]
        user_id = user_id.encode()
        user_id = hashlib.sha256(user_id).hexdigest()
        desktop_layout = int(user_id[0:10], 16) % 8
        mobile_layout = int(user_id[10:20], 16) % 4

        # Display stories
        stories = get_stories()
        return render_template('index.html', stories=stories,
                                desktop_layout=desktop_layout,
                                mobile_layout = mobile_layout)


@app.route('/left/', methods = ['GET', 'POST'])
def left():
    """Display left-leaning sources and log page events from POST requests."""

    # Log data from POST requests
    if request.method == "POST":
        log_event(request)
        return make_response(jsonify({"message":"ok"}), 200)
    
    # Display page for GET requests
    else:
        
        # Determine CCPA banner configuration based on user IP
        user_id = str(request.remote_addr)[2:-1]
        user_id = user_id.encode()
        user_id = hashlib.sha256(user_id).hexdigest()
        desktop_layout = int(user_id[0:10], 16) % 8
        mobile_layout = int(user_id[10:20], 16) % 4

        # Get stories from selected sources and display
        stories = get_stories(sources = ["The Huffington Post", "Politico"])
        return render_template('left.html', stories=stories, 
                                desktop_layout=desktop_layout,
                                mobile_layout = mobile_layout)


@app.route('/center/', methods = ['GET', 'POST'])
def center():
    """Display cener-leaning sources and log page events from POST requests."""

     # Log data from POST requests
    if request.method == "POST":
        log_event(request)
        return make_response(jsonify({"message":"ok"}), 200)
    
    # Display page for GET requests
    else:
        
        # Determine CCPA banner configuration based on user IP
        user_id = str(request.remote_addr)[2:-1]
        user_id = user_id.encode()
        user_id = hashlib.sha256(user_id).hexdigest()
        desktop_layout = int(user_id[0:10], 16) % 8
        mobile_layout = int(user_id[10:20], 16) % 4

        # Get stories from selected sources and display
        stories = get_stories(sources = ["USA Today", "CNN"])
        return render_template('center.html', stories=stories,
                                desktop_layout=desktop_layout,
                                mobile_layout = mobile_layout)


@app.route('/right/', methods = ['GET', 'POST'])
def right():
    """Display right-leaning sources and log page events from POST requests."""

     # Log data from POST requests
    if request.method == "POST":
        log_event(request)
        return make_response(jsonify({"message":"ok"}), 200)
    
    # Display page
    else:

        # Determine CCPA banner configuration based on user IP
        user_id = str(request.remote_addr)[2:-1]
        user_id = user_id.encode()
        user_id = hashlib.sha256(user_id).hexdigest()
        desktop_layout = int(user_id[0:10], 16) % 8
        mobile_layout = int(user_id[10:20], 16) % 4

        # Get stories from selected sources and display
        stories = get_stories(sources = ["Breitbart News", "The Washington Times"])
        return render_template('right.html', stories=stories,
                                desktop_layout=desktop_layout,
                                mobile_layout = mobile_layout)


@app.route('/international/', methods = ['GET', 'POST'])
def international():
    """Display international sources and log page events from POST requests."""

     # Log data from POST requests
    if request.method == "POST":
        log_event(request)
        return make_response(jsonify({"message":"ok"}), 200)
    
    # Display page during GET requests
    else:

        # Determine CCPA banner configuration based on user IP
        user_id = str(request.remote_addr)[2:-1]
        user_id = user_id.encode()
        user_id = hashlib.sha256(user_id).hexdigest()
        desktop_layout = int(user_id[0:10], 16) % 8
        mobile_layout = int(user_id[10:20], 16) % 4

        # Get stories from selected sources and display
        stories = get_stories(sources = ["BBC News", "Reuters", "Al Jazeera English"])
        return render_template('international.html', stories=stories,
                                desktop_layout=desktop_layout,
                                mobile_layout = mobile_layout)


@app.route('/privacypolicy/', methods = ['GET', 'POST'])
def privacy_policy():
    """Displays privacy policy and provides method to opt-out from the study"""

    # Log data from POST requests
    if request.method == "POST":
        log_event(request)
        return make_response(jsonify({"message":"ok"}), 200)

    # Display page
    else:
        return render_template('privacypolicy.html')


@app.route('/optout/')
def opt_out():
    """Page to indicate user has opted out of the study."""
    return render_template('optout.html')


if __name__ == "__main__":
    """Run dev server."""

    # Run Flask server
    app.run(debug=True)