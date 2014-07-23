from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)

meta = db.MetaData()
meta.bind = db.engine

import models

def fetch_incidents_at_address(address):
    fire_query = db.session.query(models.FireIncident).filter(models.FireIncident.incident_address==address.upper())
    police_query = db.session.query(models.PoliceIncident).filter(models.PoliceIncident.incident_address==address.upper())
    business_query = db.session.query(models.BusinessLicense).filter(models.BusinessLicense.business_address==address.upper())

    return {
        'fire': fire_query.all(),
        'police': police_query.all(),
        'businesses': business_query.all()
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
