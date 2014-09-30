AddressIQ
=====================

This dashboard analyzes data in order to help identify emergency resource super-utilizers and support finding cost-effective ways to give them better care.

This app is being developed by Team Long Beach for Long Beach, California. It's a work in progress.

What this data can and can't tell us
------------------------------------
The actual data we've been analyzing is not included in this repo. Still, it's worth noting what it can and can't tell us.

This data can't tell us about individuals, it can only tell us about addresses. The development and any findings must be framed accordingly.

Installation
------------

This is a Python Flask application. To install Python in your local development environment, follow the directions for [Python & Virtualenv](https://github.com/codeforamerica/howto/blob/master/Python-Virtualenv.md). The file `Procfile` contains the command for running the app; you can run it directly:

    $ python app.py

...or ask [Honcho](http://honcho.readthedocs.org/) to run it for you:

    $ pip install honcho
    $ honcho start

Note that you'll need the following environment variables set:

- APP_SETTINGS: you probably want this to equal `Config.DevelopmentConfig`
- SECRET_KEY: Follow the instructions [here](http://flask.pocoo.org/docs/quickstart/) under "How to generate good secret keys"
- DATABASE_URI: This is a string representing your database's URI.
- MAINTENANCE_MODE: Setting this to "on" will activate maintenance mode, directing all traffic to a "down for maintenance" page.

To keep these set regularly, you might want to either create a shell script or use virtualenvwrapper and a postactivate script, as described [here](http://www.realpython.com/blog/python/flask-by-example-part-1-project-setup/).

Testing
------
To view on your local machine:

1. Type this to activate the virtual environment:
        `source ENV/bin/activate`
2. Type this to activate the framework:
        `python app.py`
3. Open your browser to `http://localhost:5000`
