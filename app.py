import flask
import sqlalchemy

from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://danielgetelman:@127.0.0.1:5432/lbc_fire_data'
app.debug = True

db = SQLAlchemy(app)

SAMPLE_QUERY = '''
SELECT address_or_intersection, 
       MAX(common_name) AS common_name, 
       COUNT(*) AS num,
       COUNT(CASE WHEN alarm_datetime > ((TIMESTAMP '12/8/2013 00:00-08') - interval '7 days') AND alarm_datetime <= TIMESTAMP '12/8/2013 00:00-08' THEN 1 ELSE NULL END) AS last7, 
       COUNT(CASE WHEN alarm_datetime > ((TIMESTAMP '12/8/2013 00:00-08') - interval '30 days') AND alarm_datetime <= TIMESTAMP '12/8/2013 00:00-08' THEN 1 ELSE NULL END) AS last30 
                            FROM fire_incidents WHERE incident_number IN 
                              (SELECT incident_number FROM fire_dispatches WHERE 
                                    (fire_dispatches.apparatus_id LIKE 'R%' OR fire_dispatches.apparatus_id LIKE 'BLS%') AND fire_dispatches.transport_time_in_sec IS NOT NULL) 
                              GROUP BY address_or_intersection ORDER BY num DESC LIMIT 50; 
'''.replace("\n", "")

SAMPLE_QUERY_NONAME = '''
SELECT address_or_intersection, 
       MAX(common_name) AS common_name, 
       COUNT(*) AS num,
       COUNT(CASE WHEN alarm_datetime > ((TIMESTAMP '12/8/2013 00:00-08') - interval '7 days') AND alarm_datetime <= TIMESTAMP '12/8/2013 00:00-08' THEN 1 ELSE NULL END) AS last7, 
       COUNT(CASE WHEN alarm_datetime > ((TIMESTAMP '12/8/2013 00:00-08') - interval '30 days') AND alarm_datetime <= TIMESTAMP '12/8/2013 00:00-08' THEN 1 ELSE NULL END) AS last30 
                            FROM fire_incidents WHERE incident_number IN 
                              (SELECT incident_number FROM fire_dispatches WHERE 
                                    (fire_dispatches.apparatus_id LIKE 'R%' OR fire_dispatches.apparatus_id LIKE 'BLS%') AND fire_dispatches.transport_time_in_sec IS NOT NULL) 
                              AND common_name IS NULL 
                              GROUP BY address_or_intersection ORDER BY num DESC LIMIT 50; 
'''.replace("\n", "")

@app.route('/')
def home():
    query = db.engine.execute(sqlalchemy.text(SAMPLE_QUERY))
    return render_template('home.html', rows=query.fetchall())

@app.route('/noname')
def noname():
    query = db.engine.execute(sqlalchemy.text(SAMPLE_QUERY_NONAME))
    return render_template('home.html', rows=query.fetchall())

@app.route('/address/<string:address>')
def address_info(address):
    ADDRESS_QUERY = '''SELECT alarm_datetime, initial_cad_call_type_description, actual_nfirs_incident_type_description, common_name, apparatus_type, apparatus_description FROM fire_incidents INNER JOIN fire_dispatches ON fire_incidents.incident_number=fire_dispatches.incident_number
                        WHERE (fire_dispatches.apparatus_id LIKE 'R%' OR fire_dispatches.apparatus_id LIKE 'BLS%') AND fire_dispatches.transport_time_in_sec IS NOT NULL
                        AND lower(:address)=lower(fire_incidents.address_or_intersection) ORDER BY alarm_datetime DESC''';

    all_calls = db.engine.execute(sqlalchemy.text(ADDRESS_QUERY), address=address).fetchall()

    return render_template('address.html', calls=all_calls, address=address, common_name=all_calls[0][3])


if __name__ == '__main__':
    app.run()
