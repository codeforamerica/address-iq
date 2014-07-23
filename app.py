from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

meta = db.MetaData()
meta.bind = db.engine

def fetch_incidents_at_address(address):
    fire_incidents = db.Table('fire_incidents', meta, autoload=True)
    police_incidents = db.Table('police_incidents', meta, autoload=True)
    business_licenses = db.Table('all_business_licenses', meta, autoload=True)
    
    fire_select = db.select([fire_incidents], fire_incidents.c.incident_address==address.upper())
    police_select = db.select([police_incidents], police_incidents.c.incident_address==address.upper())
    business_licenses_select = db.select([business_licenses], business_licenses.c.business_address==address.upper())

    return {
        'fire': fire_select.execute().fetchall(),
        'police': police_select.execute().fetchall(),
        'businesses': business_licenses_select.execute().fetchall()
    }

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/address/<address>")
def address(address):
    incidents = fetch_incidents_at_address(address)
    return "%d fire incidents" % len(incidents['fire'])

if __name__ == "__main__":
    app.run(debug=True)
