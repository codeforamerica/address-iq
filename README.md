AddressIQ
=====================

AddressIQ is a web application that analyzes city data to help identify addresses with a high number of 911 calls and support finding cost-effective ways to provide those addresses with better care and resources.

View the [AddressIQ User Manual](https://docs.google.com/a/codeforamerica.org/presentation/d/1gSuvhTcUj2y-2w-lBtxw6iCQXXlI2RY5x4C461OhgMs/edit#slide=id.p) for a walkthrough of how the app works and what it looks like.

Read [AddressIQ 101 Documentation](https://docs.google.com/a/codeforamerica.org/document/d/1sC7tCxGHRgozcPbNPNoY56ggey4JkxJOQqx8acHQOMs/edit) for more in-depth background of the problem AddressIQ is trying to solve and information about health hot spotting.

Read [our End of Year Report](https://docs.google.com/document/d/1gVUR94EG5LQx_zzjhNUrOtGssinEd8iqPpOczmksiO4/edit?usp=sharing) for the most in-depth coverage of our fellowship journey and how we came to develop AddressIQ.

This project was developed by Code for America fellows (@dget, @fureigh, and @mollymcleod) for Long Beach, California.

For more context, watch our [five-minute talk](https://www.youtube.com/watch?v=TxifmeeFT2s) from the 2014 Code for America Summit.

What this data can and can't tell us
------------------------------------
The actual data we analyzed is not included in this repo. This data can't tell us about individuals, it can only tell us about addresses. The development and any findings must be framed accordingly.

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

If using [Aptible](https://www.aptible.com), here's the command to run to activate maintenance mode: `aptible config:set MAINTENANCE_MODE=on`

Testing
------
To view on your local machine:

1. Type this to activate the virtual environment:
        `source ENV/bin/activate`
2. Type this to activate the framework:
        `python app.py`
3. Open your browser to `http://localhost:5000`
