import argparse
from sqlalchemy import create_engine
from transformer import transform

table_name = 'fire_incidents'
transformations = []

def remove_900X(row):
    ''' Remove calls with types in the 900-range, which aren't relevant for us '''
    if row.actual_nfirs_incident_type_description and row.actual_nfirs_incident_type_description[0] == '9':
        return None
    else:
        return row


transformations.append(remove_900X)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Transform a database')
    parser.add_argument('--hostdb')
    parser.add_argument('--destinationdb')
    args = parser.parse_args()

    host_engine = create_engine(args.hostdb)
    dest_engine = create_engine(args.destinationdb)

    transform(host_engine, dest_engine, table_name, transformations)
