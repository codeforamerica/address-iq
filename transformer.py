# interface: 
# `transformer --hostdb=dbstring1 --destinationdb=dbstring2 transformation.py`
# `python fire_transformation.py --hostdb=dbstring1 --destinationdb=dbstring2`

import argparse
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy.sql import select, insert

host_db = None
destination_db = None

meta = MetaData()

def transform(host_engine, dest_engine, table_name, transformations):
    host_table = Table(table_name, meta, autoload=True, autoload_with=host_engine)

    print "Fetching rows..."
    results = host_engine.execute(select([host_table]))

    print "Beginning transformation..."
    transformed_rows = []
    for row in results:
        if len(transformed_rows) % 10000 == 0:
            print "Row #: ", len(transformed_rows)

        new_row = row
        
        # Run all transformations, stopping if one returns None
        for f in transformations:
            new_row = f(new_row)
            if new_row == None:
                break

        if new_row != None:
            transformed_rows.append(new_row)

    print "Getting ready to insert..."
    dest_table = Table(table_name, meta, autoload=True, autoload_with=dest_engine)  
    dest_engine.execute(dest_table.insert(), transformed_rows)

