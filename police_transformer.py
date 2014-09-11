import argparse
from sqlalchemy import create_engine
from transformer import transform

table_name = 'police_incidents'
transformations = []

def remove_clb_ending(row):
    address = row.incident_address

    if ', CLB' == address[-5:]:
        row.incident_address = address[:-5]

    return row

transformations.append(remove_clb_ending)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Transform a database')
    parser.add_argument('--hostdb')
    parser.add_argument('--destinationdb')
    args = parser.parse_args()

    host_engine = create_engine(args.hostdb)
    dest_engine = create_engine(args.destinationdb)

    transform(host_engine, dest_engine, table_name, transformations)
