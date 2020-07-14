(Last updated 7/13)
Overview:
This is a simple website designed to study user interaction with California Consumer Privacy Act
"Do Not Sell My Information" notices, and the effect of user interface design on this interaction.
The website displays top news stories from a variety of sources across the US political spectrum,
as well as international media outlets.  It also displays a CCPA notice in a location determined
randomly by the user's IP address.  User interactions with the website are logged.

Set-up guide:
1. Install required python packages.  A list of these dependencies, available through PIP, can be found in "requirements.txt".
2. Initialize the SQL database tables.  Do this by running a python shell in the example_site directory, then run the following commands:
	* from app import db
	* db.create_all()
3. To test on localhost, run "app.py."  If you wish to record logs to a file, redirect output when running like so:
	python app.py > filename.csv
	Otherwise all events will be logged in the python console.
4. Visit the site at http://localhost:5000/ 


Guide to files:

**example_site:
app.py - back-end FLASK server functionality
userdata.py - Currently deprecated, previously contained class for logging data.
static/js/scripts.js - front end javascript to log user interaction
static/js/main.js - javascript displaying CCPA notice
templates/base.html - base HTML template including common scripts
templates/index.html - homepage displaying all news stories
templates/center.html - page filtering stories from centrist sources
templates/left.html - page filtering stories from left-leaning sources
templates/right.html - page filtering stories from right-leaning sources
templates/international.html - page filtering stories from international sources
templates/privacypolicy.html - page with study privacy disclosures and option to opt-out
templates/optout.html - page indicating user has successfully opted out of the study.

**userstudy-website:
readme.txt - this file
requirements.txt - python dependencies for app.py, available through PIP
last_updated.txt - logs time since news stories were last refreshed from the web