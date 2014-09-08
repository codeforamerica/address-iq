import datetime
from datetime import timedelta
import os
import operator
import pytz
import logging
import sqlalchemy.exc
from logging.handlers import RotatingFileHandler

from flask import Flask, render_template, abort, request, Response, session, redirect, url_for, make_response
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required
from flask.ext.seasurf import SeaSurf
from functools import wraps

from requests import post

from gdata.spreadsheets.client import SpreadsheetsClient
from oauth2client.client import SignedJwtAssertionCredentials
from gdata.gauth import OAuth2TokenFromCredentials

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.permanent_session_lifetime = timedelta(minutes=15)
db = SQLAlchemy(app)

meta = db.MetaData()
meta.bind = db.engine

activated_table = db.Table('activated_addresses', meta,
                            db.Column('address', db.String, primary_key=True))

csrf = SeaSurf(app)

import models

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login_page"

@app.before_request
def func():
  session.modified = True


@login_manager.user_loader
def load_user(userid):
    if not userid:
        return None
    try:
        userid = int(userid)
    except ValueError:
        app.logger.error('There was a ValueError in load_user.')
        return None

    return models.User.query.get(userid)

def audit_log(f):
    @wraps(f)

    def decorated_function(*args, **kwargs):
        auditing_disabled = app.config.get('AUDIT_DISABLED', app.config.get('TESTING', False))
        if auditing_disabled:
            return f(*args, **kwargs)

        response = make_response(f(*args, **kwargs))

        log_info = {
            "resource": request.path,
            "method": request.method,
            "response_code": response.status_code,
            "user_id": current_user.get_id()
        }
        log_entry = models.AuditLogEntry(**log_info)
        db.session.add(log_entry)
        db.session.commit()

        return response

    return decorated_function

def fetch_incidents_at_address(address):
    fire_query = db.session.query(models.FireIncident)
    fire_query = fire_query.filter(models.FireIncident.incident_address == address.upper())

    police_query = db.session.query(models.PoliceIncident)
    police_query = police_query.filter(models.PoliceIncident.incident_address == address.upper())

    business_query = db.session.query(models.BusinessLicense)
    business_query = business_query.filter(models.BusinessLicense.business_address == address.upper())

    return {
        'fire': fire_query.all(),
        'police': police_query.all(),
        'businesses': business_query.all()
    }


def count_incidents_by_timeframes(incidents, timeframes):
    def start_date_for_days(days):
        return datetime.date.today() - datetime.timedelta(days=days)

    # dates to look for events after for each timeframe
    timeframes_info = [{"days": days,
                        "start_date": start_date_for_days(days)
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
                if incident_date > timeframe_info['start_date']:
                    counts[incident_type][timeframe_info['days']] = \
                        counts[incident_type][timeframe_info['days']] + 1

    return counts

def get_top_incident_reasons_by_timeframes(incidents, timeframes):
    def start_date_for_days(days):
        return datetime.date.today() - datetime.timedelta(days=days)

    # dates to look for events after for each timeframe
    timeframes_info = [{"days": days,
                        "start_date": start_date_for_days(days)
                        } for days in timeframes]

    counts = {'fire': {}, 'police': {}}

    # count how many of each incident type happen in each timeframe
    for incident_type in counts:
        if incident_type == 'fire':
            reason_field = 'actual_nfirs_incident_type_description'
        else:
            reason_field = 'final_cad_call_type_description'

        if incident_type == 'fire':
            date_field = 'alarm_datetime'
        else:
            date_field = 'call_datetime'

        for timeframe in timeframes:
            counts[incident_type][timeframe] = {}

        for incident in incidents[incident_type]:
            incident_date = getattr(incident, date_field).date()
            incident_reason = getattr(incident, reason_field)
            for timeframe_info in timeframes_info:
                if incident_date > timeframe_info['start_date']:
                    relevant_reasons_table = counts[incident_type][timeframe_info['days']]

                    if incident_reason in relevant_reasons_table:
                        relevant_reasons_table[incident_reason] = relevant_reasons_table[incident_reason] + 1
                    else:
                        relevant_reasons_table[incident_reason] = 1

    top_call_types = {'fire': {}, 'police': {}}
    for incident_type in top_call_types:
        for timeframe_info in timeframes_info:
            num_days = timeframe_info['days']
            top_call_types[incident_type][num_days] = sorted(counts[incident_type][num_days].iteritems(),
                                                             key=operator.itemgetter(1))
            top_call_types[incident_type][num_days].reverse()
            top_call_types[incident_type][num_days] = top_call_types[incident_type][num_days][:5]

    return top_call_types

@app.route('/')
def home():
    return render_template('home.html', email=get_email_of_current_user())

@app.route('/log-in', methods=['GET'])
def login_page():
    next = request.args.get('next')
    return render_template('login.html', next=next, email=get_email_of_current_user())

def fetch_authorization_row(email):
    CLIENT_EMAIL = app.config['GOOGLE_CLIENT_EMAIL']
    PRIVATE_KEY = app.config['GOOGLE_PRIVATE_KEY']

    SCOPE = "https://spreadsheets.google.com/feeds/"
    
    credentials = SignedJwtAssertionCredentials(CLIENT_EMAIL, PRIVATE_KEY, SCOPE)
    token = OAuth2TokenFromCredentials(credentials)
    client = SpreadsheetsClient()

    token.authorize(client)

    # Load worksheet with auth info
    spreadsheet_id = app.config['GOOGLE_SPREADSHEET_ID']
    worksheets = client.get_worksheets(spreadsheet_id)
    worksheet = worksheets.entry[0]

    # worksheet.id.text takes the form of a full url including the spreadsheet, while
    # we only need the last part of that
    id_parts = worksheet.id.text.split('/')
    worksheet_id = id_parts[len(id_parts) - 1]

    list_feed = client.get_list_feed(spreadsheet_id, worksheet_id)

    rows = [row.to_dict() for row in list_feed.entry]

    user_auth_row = None
    for row in rows:
        if row['email'] == email:
            user_auth_row = row
            break

    return user_auth_row

@app.route('/log-in', methods=['POST'])
@csrf.exempt
def log_in():
    posted = post('https://verifier.login.persona.org/verify',
                  data=dict(assertion=request.form.get('assertion'),
                            audience=app.config['BROWSERID_URL']))

    response = posted.json()

    if response.get('status', '') == 'okay':
        email = response['email']
        user_auth_row = fetch_authorization_row(email)

        if not user_auth_row or user_auth_row['canviewsite'] != 'Y':
            return 'Not authorized', 403

        user = load_user_by_email(email)

        if not user:
            user = create_user(email, user_auth_row['name'])

        login_user(user)
        return 'OK'

    return Response('Failed', status=400)

@app.route("/browse")
@login_required
@audit_log
def browse():
    date_range = int(request.args.get('date_range', 365))
    page = int(request.args.get('page', 1))

    sort_by = request.args.get('sort_by', 'fire')
    sort_order = request.args.get('sort_order', 'desc')

    order_column_map = {
        'address': getattr(models.AddressSummary, 'address'),
        'fire': getattr(models.AddressSummary, 'fire_incidents_last%d' % date_range),
        'police': getattr(models.AddressSummary, 'police_incidents_last%d' % date_range)
    }
    order_column = order_column_map.get(sort_by, order_column_map['fire'])

    if sort_order == 'asc':
        order_column = order_column.asc()
    else:
        order_column = order_column.desc()

    summaries = models.AddressSummary.query
    summaries = summaries.order_by(order_column).paginate(page, per_page=10)

    return render_template("browse.html", summaries=summaries, date_range=date_range,
        sort_by=sort_by, sort_order=sort_order, email=get_email_of_current_user())


@csrf.exempt
@app.route('/log-out', methods=['POST'])
def log_out():
    logout_user()

    return redirect(url_for('home'))

def create_user(name, email):
    # Check whether a record already exists for this user.
    user = models.User.query.filter(models.User.email==email).first()
    if user:
        return False

    # If no record exists, create the user.
    user = models.User(name=name, email=email, date_created=datetime.datetime.now(pytz.utc))
    db.session.add(user)
    db.session.commit()

    return user

def load_user_by_email(email):
    user = models.User.query.filter(models.User.email==email).first()

    return user

def get_email_of_current_user(user=current_user):
    if user.is_anonymous():
        return None

    email = user.email

    if not email:
        return None

    return email

def is_address_activated(address):
    address_query = db.session.query(activated_table).filter(activated_table.c.address == address)

    return db.session.query(address_query.exists()).scalar()

def activate_address(address):
    query = activated_table.insert().values(address=address)
    db.session.execute(query)

    action = models.Action(user_id=current_user.id, type="activated", address=address)
    db.session.add(action)
    db.session.commit()

def deactivate_address(address):
    query = activated_table.delete().where(activated_table.c.address == address)
    db.session.execute(query)

    action = models.Action(user_id=current_user.id, type="deactivated", address=address)
    db.session.add(action)
    db.session.commit()

@app.route("/address/<address>")
@login_required
@audit_log
def address(address):
    incidents = fetch_incidents_at_address(address)

    if len(incidents['fire']) == 0 and len(incidents['police']) == 0:
        abort(404)

    counts = count_incidents_by_timeframes(incidents, [7, 30, 90, 365])
    business_types = [biz.business_service_description.strip() for biz in incidents['businesses']]
    business_names = [biz.name.strip() for biz in incidents['businesses']]
    top_call_types = get_top_incident_reasons_by_timeframes(incidents, [7, 30, 90, 365])
    actions = models.Action.query.filter(models.Action.address==address).order_by(models.Action.created).all()
    activated = is_address_activated(address)

    kwargs = dict(email=get_email_of_current_user(), incidents=incidents, counts=counts,
                           business_types=business_types, business_names=business_names,
                           top_call_types=top_call_types, address=address, actions=actions,
                           activated=activated)

    return render_template('address.html', **kwargs)

@app.route("/address/<address>/comments", methods=['POST'])
@login_required
@audit_log
def post_comment(address):
    comment = request.form.get('content')

    if not comment:
        return redirect(url_for("address", address=address))

    comment = models.Action(user_id=current_user.id, type="comment", content=comment, address=address)
    db.session.add(comment)
    db.session.commit()

    return redirect(url_for("address", address=address))

@app.route("/address/<address>/activate", methods=["POST"])
@login_required
def activate(address):
    try: 
        activate_address(address)
        db.session.commit()
        return 'activated'
    except sqlalchemy.exc.IntegrityError:
        return 'already activated', 400

@app.route("/address/<address>/deactivate", methods=["POST"])
@login_required
def deactivate(address):
    deactivate_address(address)
    db.session.commit()
    return 'deactivated'


@app.route("/audit_log")
@login_required
@audit_log
def view_audit_log():
    page = int(request.args.get('page', 1))


    log_entries = models.AuditLogEntry.query
    log_entries = log_entries.order_by(models.AuditLogEntry.timestamp.desc())

    return render_template("audit_log.html", email=current_user.email, entries=log_entries.paginate(page, per_page=100))

if __name__ == "__main__":
    handler = RotatingFileHandler('errors.log', maxBytes=10000, backupCount=20)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(debug=True)
