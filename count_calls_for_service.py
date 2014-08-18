from app import db
from models import FireIncident, PoliceIncident, BusinessLicense, AddressSummary
import pytz

import datetime

DEFAULT_TIMEFRAMES = [7, 14, 30, 60, 90, 180, 365, 730]

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
                       'fire_counts', DEFAULT_TIMEFRAMES)

def count_police_calls(incidents):
    return count_calls(incidents, 'call_datetime', 
                       'police_counts', DEFAULT_TIMEFRAMES)

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

    summaries = [address_counts_dict_to_call_summary(address, counts) for address, counts in addresses.iteritems()]
    db.session.query(AddressSummary).delete()
    [db.session.add(summary) for summary in summaries]
    db.session.commit()