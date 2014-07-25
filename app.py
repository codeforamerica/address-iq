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

def count_incidents_by_timeframes(incidents, timeframes):
    import datetime
    # dates to look for events after for each timeframe
    timeframes_info = [{"days": days,
                        "cutoff_date": datetime.date.today() - datetime.timedelta(days=days)
                    } for days in timeframes]

    counts = {'fire': {}, 'police': {}}

    for incident_type in counts:
        if incident_type == 'fire':
            date_field = 'alarm_datetime'
        else:
            date_field = 'call_datetime'

        for timeframe in timeframes:
            counts[incident_type][timeframe] = 0

        for incident in incidents[incident_type]:
            incident_date = getattr(incident, date_field).date()
            for timeframe_info in timeframes_info:
                if incident_date > timeframe_info['cutoff_date']:
                    counts[incident_type][timeframe_info['days']] = counts[incident_type][timeframe_info['days']] + 1

    return counts
    

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/address/<address>")
def address(address):
    incidents = fetch_incidents_at_address(address)
    counts = count_incidents_by_timeframes(incidents, [7, 30, 90, 365])
    return render_template("address.html", incidents=incidents, counts=counts)

if __name__ == "__main__":
    app.run(debug=True)
