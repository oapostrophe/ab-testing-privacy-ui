(Last updated 6/9)
Guide to files:
requirements.txt - list of python PIP packages required, generated with "pip freeze".

example_site/
	app.py - Core code for webapp, run "python app.py" to start flask local server
	test.db - SQLite database of top stories last retrieved
	templates / 
		index.html - homepage displaying news stories
		base.html - boilerplate html page template