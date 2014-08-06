from app import db
from models import FireIncident, PoliceIncident, BusinessLicense
import pytz

import datetime

year_ago = datetime.datetime.now(pytz.utc) - datetime.timedelta(days=365)

fire_incidents_query = db.session.query(FireIncident)
fire_incidents_query = fire_incidents_query.filter(FireIncident.alarm_datetime >= year_ago)

def count_fire_calls(fire_incidents):
    timeframes = {
        7: None,
        30: None,
        90: None,
        365: None
    }
    for num_days in timeframes:
        start_date = datetime.datetime.now(pytz.utc) - datetime.timedelta(days=num_days)
        timeframes[num_days] = {
            'start_date': start_date,
        }

    addresses = {}

    for incident in fire_incidents:
        if incident.incident_address not in addresses:
            addresses[incident.incident_address] = {
                7: 0,
                30: 0,
                90: 0,
                365: 0
            }

        address_counts = addresses[incident.incident_address]

        for num_days in timeframes:
            if incident.alarm_datetime > timeframes[num_days]['start_date']:
                address_counts[num_days] = address_counts[num_days] + 1

    return addresses

fire_incidents = fire_incidents_query.all()
print count_fire_calls(fire_incidents)
