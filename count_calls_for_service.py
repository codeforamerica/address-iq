from app import db
from models import FireIncident, PoliceIncident, BusinessLicense, AddressSummary
import pytz

import datetime


def count_calls(incidents, time_field, output_header, timeframes):
    start_dates = {}

    for num_days in timeframes:
        start_date = datetime.datetime.now(pytz.utc) - datetime.timedelta(days=num_days)
        start_dates[num_days] = start_date

    addresses = {}

    for incident in incidents:
        if incident.incident_address.strip() not in addresses:
            addresses[incident.incident_address.strip()] = {}
            empty_counts = dict([(num_days, 0) for num_days in timeframes])
            addresses[incident.incident_address.strip()][output_header] = empty_counts

        address_counts = addresses[incident.incident_address.strip()][output_header]

        for num_days in timeframes:
            if getattr(incident, time_field) > start_dates[num_days]:
                address_counts[num_days] = address_counts[num_days] + 1

    return addresses

def count_fire_calls(incidents):
    return count_calls(incidents, 'alarm_datetime', 
                       'fire_counts', [7, 14, 30, 60, 90, 180, 365, 730])

def count_police_calls(incidents):
    return count_calls(incidents, 'call_datetime', 
                       'police_counts', [7, 14, 30, 60, 90, 180, 365, 730])

def fetch_businesses_for_addresses(addresses):
    license_query = db.session.query(BusinessLicense).filter(BusinessLicense.business_address.in_(addresses))
    licenses = license_query.all()

    import itertools
    biz_addresses = {}
    for license in licenses:
        if license.business_address in addresses:
            biz_addresses[license.business_address.strip()].append(license)
        else:
            biz_addresses[license.business_address.strip()] = [license]

    return biz_addresses

two_years_ago = datetime.datetime.now(pytz.utc) - datetime.timedelta(days=730)

fire_incidents_query = db.session.query(FireIncident)
fire_incidents_query = fire_incidents_query.filter(FireIncident.alarm_datetime >= two_years_ago)
fire_incidents = fire_incidents_query.all()
addresses = count_fire_calls(fire_incidents)

police_incidents_query = db.session.query(PoliceIncident)
police_incidents_query = police_incidents_query.filter(PoliceIncident.call_datetime >= two_years_ago)
police_incidents = police_incidents_query.all()
police_addresses = count_police_calls(police_incidents)

for address in police_addresses:
    if address.strip() not in addresses:
        addresses[address.strip()] = police_addresses[address.strip()]
    else:
        addresses[address.strip()].update(police_addresses[address.strip()])

business_addresses =  fetch_businesses_for_addresses(addresses.keys())

for address in addresses:
    address_record = addresses[address.strip()]
    if address.strip() not in business_addresses:
        address_record['business_count'] = 0
        address_record['business_names'] = ''
        address_record['business_types'] = ''

    else:
        address_record['business_count'] = len(business_addresses[address.strip()])
        address_record['business_names'] = [', '.join([biz.name for biz in business_addresses[address.strip()]])]
        address_record['business_types'] = [', '.join([biz.business_service_description for biz in business_addresses[address.strip()]])]

def address_counts_dict_to_call_summary(address, counts):
    row = {
        'address': address.strip()
    }

    if 'fire_counts' in counts:
        row['fire_last7'] = counts['fire_counts'][7]
        row['fire_prior7'] = counts['fire_counts'][14] - counts['fire_counts'][7]
        row['fire_last30'] = counts['fire_counts'][30]
        row['fire_prior30'] = counts['fire_counts'][60] - counts['fire_counts'][30]
        row['fire_last90'] = counts['fire_counts'][90]
        row['fire_prior90'] = counts['fire_counts'][180] - counts['fire_counts'][90]
        row['fire_last365'] = counts['fire_counts'][365]
        row['fire_prior365'] = counts['fire_counts'][730] - counts['fire_counts'][365]
    else:
        row['fire_last7'] = 0
        row['fire_prior7'] = 0
        row['fire_last30'] = 0
        row['fire_prior30'] = 0
        row['fire_last90'] = 0
        row['fire_prior90'] = 0
        row['fire_last365'] = 0
        row['fire_prior365'] = 0

    if 'police_counts' in counts:
        row['police_last7'] = counts['police_counts'][7]
        row['police_prior7'] = counts['police_counts'][14] - counts['police_counts'][7]
        row['police_last30'] = counts['police_counts'][30]
        row['police_prior30'] = counts['police_counts'][60] - counts['police_counts'][30]
        row['police_last90'] = counts['police_counts'][90]
        row['police_prior90'] = counts['police_counts'][180] - counts['police_counts'][90]
        row['police_last365'] = counts['police_counts'][365]
        row['police_prior365'] = counts['police_counts'][730] - counts['police_counts'][365]
    else:
        row['police_last7'] = 0
        row['police_prior7'] = 0
        row['police_last30'] = 0
        row['police_prior30'] = 0
        row['police_last90'] = 0
        row['police_prior90'] = 0
        row['police_last365'] = 0
        row['police_prior365'] = 0

    return AddressSummary(**row)

summaries = [address_counts_dict_to_call_summary(address, counts) for address, counts in addresses.iteritems()]
db.session.query(AddressSummary).delete()
[db.session.add(summary) for summary in summaries]
db.session.commit()