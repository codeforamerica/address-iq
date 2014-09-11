from app import db
from models import FireIncident, PoliceIncident, BusinessLicense, AddressSummary
import pytz

import datetime

DEFAULT_TIMEFRAMES = [7, 14, 30, 60, 90, 180, 365]

def count_calls(incidents, time_field, output_header, timeframes):
    start_dates = {}

    for num_days in timeframes:
        start_date = datetime.datetime.now(pytz.utc) - datetime.timedelta(days=num_days)
        start_dates[num_days] = start_date

    addresses = {}

    for incident in incidents:
        address = incident[0].strip()
        if ', CLB' == address[-5:]:
            address = address[:-5]

        incident_date = incident[1]

        if address not in addresses:
            addresses[address] = {}
            empty_counts = dict([(num_days, 0) for num_days in timeframes])
            addresses[address][output_header] = empty_counts

        address_counts = addresses[address][output_header]

        for num_days in timeframes:
            if incident_date > start_dates[num_days]:
                address_counts[num_days] = address_counts[num_days] + 1

    return addresses

def count_fire_calls(incidents):
    return count_calls(incidents, 'alarm_datetime', 
                       'fire_counts', DEFAULT_TIMEFRAMES)

def count_police_calls(incidents):
    return count_calls(incidents, 'call_datetime', 
                       'police_counts', DEFAULT_TIMEFRAMES)

def address_counts_dict_to_call_summary(address, counts):
    row = {
        'address': address.strip()
    }

    model_timeframes = [7, 30, 90, 365]

    for department in ['fire', 'police']:
        count_field = department + '_counts'

        if count_field in counts:
            for days_ago in model_timeframes:
                row['%s_incidents_last%d' % (department, days_ago)] = counts[count_field][days_ago]
                row['%s_incidents_prev%d' % (department, days_ago)] = counts[count_field][days_ago] * 2 - counts[count_field][days_ago]
        else:
            for days_ago in model_timeframes:
                row['%s_incidents_last%d' % (department, days_ago)] = 0
                row['%s_incidents_prev%d' % (department, days_ago)] = 0

    return AddressSummary(**row)

if __name__ == '__main__':
    two_years_ago = datetime.datetime.now(pytz.utc) - datetime.timedelta(days=370)

    print "Loading Fire Data..."
    fire_incidents_query = db.session.query(db.func.max(FireIncident.incident_address), 
                                            db.func.max(FireIncident.alarm_datetime))
    fire_incidents_query = fire_incidents_query.filter(FireIncident.alarm_datetime >= two_years_ago)
    fire_incidents_query = fire_incidents_query.group_by(FireIncident.cad_call_number)
    fire_incidents = fire_incidents_query.all()
    print "Fire Data Loaded..."
    addresses = count_fire_calls(fire_incidents)
    print "Fire Data Counted..."

    print "Loading Police Data..."
    police_incidents_query = db.session.query(db.func.max(PoliceIncident.incident_address), 
                                              db.func.max(PoliceIncident.call_datetime))
    police_incidents_query = police_incidents_query.filter(PoliceIncident.call_datetime >= two_years_ago)
    police_incidents_query = police_incidents_query.group_by(PoliceIncident.cad_call_number)
    police_incidents = police_incidents_query.all()
    print "Police Data Loaded..."
    police_addresses = count_police_calls(police_incidents)
    print "Police Data Counted..."

    for address in police_addresses:
        if address.strip() not in addresses:
            addresses[address.strip()] = police_addresses[address.strip()]
        else:
            addresses[address.strip()].update(police_addresses[address.strip()])

    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    summaries = [address_counts_dict_to_call_summary(address, counts) for address, counts in addresses.iteritems() if len(address) > 0 and address[0] in numbers]
    db.session.query(AddressSummary).delete()
    [db.session.add(summary) for summary in summaries]
    db.session.commit()