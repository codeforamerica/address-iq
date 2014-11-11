import datetime

from app import db


class FireIncident(db.Model):
    __bind_key__ = 'lbc_data'

    __tablename__ = 'standardized_fire_incidents'
    cad_call_number = db.Column(db.Integer, primary_key=True)
    incident_number = db.Column(db.Integer)
    alarm_datetime = db.Column(db.DateTime(timezone=True))

    district = db.Column(db.String(6))
    x_coordinate = db.Column(db.String(7))
    y_coordinate = db.Column(db.String(7))

    street_number = db.Column(db.String(10))
    street_prefix = db.Column(db.String(30))
    street_name = db.Column(db.String(200))
    street_type = db.Column(db.String(20))
    street_suffix = db.Column(db.String(20))

    cross_street_prefix = db.Column(db.String(30))
    cross_street_name = db.Column(db.String(200))
    cross_street_type = db.Column(db.String(20))
    cross_street_suffix = db.Column(db.String(20))

    incident_address = db.Column(db.String(255))
    apartment_number = db.Column(db.String(20))
    incident_cross_street = db.Column(db.String(255))
    postal_code = db.Column(db.String(10))

    common_name = db.Column(db.String(200))

    initial_cad_call_type = db.Column(db.String(20))
    initial_cad_call_type_description = db.Column(db.String(100))

    final_cad_call_type = db.Column(db.String(20))
    final_cad_call_type_description = db.Column(db.String(100))

    actual_nfirs_incident_type = db.Column(db.String(20))
    actual_nfirs_incident_type_description = db.Column(db.String(100))

    intersection = db.Column(db.String(6))
    standardized_address = db.Column(db.String)


class FireDispatch(db.Model):
    __bind_key__ = 'lbc_data'
    __tablename__ = 'fire_dispatches'

    incident_number = db.Column(db.Integer, primary_key=True)

    apparatus_id = db.Column(db.String(6), primary_key=True)
    apparatus_type = db.Column(db.String(3))
    apparatus_description = db.Column(db.String(100))

    dispatch_datetime = db.Column(db.String(30))
    enroute_scene_datetime = db.Column(db.String(30))
    arrival_datetime = db.Column(db.String(30))
    depart_scene_datetime = db.Column(db.String(30))
    arrived_facility_datetime = db.Column(db.String(30))
    clear_datetime = db.Column(db.String(30))

    turnout_time_in_sec = db.Column(db.Integer)
    travel_time_nfpa_response_time_in_sec = db.Column(db.Integer)
    response_time_in_sec = db.Column(db.Integer)
    total_response_time_in_sec = db.Column(db.Integer)
    on_scene_time_where_transport_in_sec = db.Column(db.Integer)
    total_on_scene_time_with_or_without_transport_in_sec = db.Column(db.Integer)
    transport_time_in_sec = db.Column(db.Integer)
    turnaround_time_in_sec = db.Column(db.Integer)
    duration_time_in_sec = db.Column(db.Integer)


class BusinessLicense(db.Model):
    __bind_key__ = 'lbc_data'
    __tablename__ = 'all_business_licenses'
    name = db.Column(db.String(200), primary_key=True)

    business_service_description = db.Column(db.String(100))
    business_product = db.Column(db.String(40))
    business_address = db.Column(db.String(200), primary_key=True)
    business_street_number = db.Column(db.String(10))
    business_street_prefix = db.Column(db.String(30))
    business_street_name = db.Column(db.String(200))
    business_street_type = db.Column(db.String(20))
    business_street_suffix = db.Column(db.String(20))
    business_zip = db.Column(db.String(20))


class PoliceIncident(db.Model):
    __bind_key__ = 'lbc_data'
    __tablename__ = 'standardized_police_incidents'

    cad_call_number = db.Column(db.String(25), primary_key=True)
    incident_number = db.Column(db.String(25))

    call_datetime = db.Column(db.DateTime(timezone=True))

    x_coordinate = db.Column(db.String(7))
    y_coordinate = db.Column(db.String(7))

    incident_address = db.Column(db.String(255))

    street_number = db.Column(db.String(10))
    street_prefix = db.Column(db.String(30))
    street_name = db.Column(db.String(200))
    street_type = db.Column(db.String(20))
    street_suffix = db.Column(db.String(20))

    initial_cad_call_type = db.Column(db.String(20))
    initial_cad_call_type_description = db.Column(db.String(100))

    final_cad_call_type = db.Column(db.String(20))
    final_cad_call_type_description = db.Column(db.String(100))

    standardized_address = db.Column(db.String)


class AddressSummary(db.Model):
    __tablename__ = 'address_summaries'

    address = db.Column(db.String(50), primary_key=True)

    fire_incidents_last7 = db.Column(db.Integer)
    fire_incidents_prev7 = db.Column(db.Integer)
    police_incidents_last7 = db.Column(db.Integer)
    police_incidents_prev7 = db.Column(db.Integer)

    fire_incidents_last30 = db.Column(db.Integer)
    fire_incidents_prev30 = db.Column(db.Integer)
    police_incidents_last30 = db.Column(db.Integer)
    police_incidents_prev30 = db.Column(db.Integer)

    fire_incidents_last90 = db.Column(db.Integer)
    fire_incidents_prev90 = db.Column(db.Integer)
    police_incidents_last90 = db.Column(db.Integer)
    police_incidents_prev90 = db.Column(db.Integer)

    # For reporting page. Six months (~30 days each)
    # We don't use prev, but without it here, count_calls will fail.
    fire_incidents_last180 = db.Column(db.Integer)
    fire_incidents_prev180 = db.Column(db.Integer)
    police_incidents_last180 = db.Column(db.Integer)
    police_incidents_prev180 = db.Column(db.Integer)

    fire_incidents_last365 = db.Column(db.Integer)
    fire_incidents_prev365 = db.Column(db.Integer)
    police_incidents_last365 = db.Column(db.Integer)
    police_incidents_prev365 = db.Column(db.Integer)

    business_count = db.Column(db.Integer, default=0)        
    business_names = db.Column(db.Text, default="")        
    business_types = db.Column(db.Text, default="")

    active = db.Column(db.Boolean)

    def counts_for_days_ago(self, days):
        return {
            'fire': {
                'last': getattr(self, "fire_incidents_last%d" % days),
                'prior': getattr(self, "fire_incidents_prev%d" % days)
            },
            'police': {
                'last': getattr(self, "police_incidents_last%d" % days),
                'prior': getattr(self, "police_incidents_prev%d" % days)
            }
        }

        
class AuditLogEntry(db.Model):
    __tablename__ = 'audit_log'

    timestamp = db.Column(db.DateTime(timezone=True), default=db.func.now(), primary_key=True)
    resource = db.Column(db.String(100), primary_key=True)
    method = db.Column(db.String(10), primary_key=True)
    response_code = db.Column(db.String(3), primary_key=True)
    user_id = db.Column(db.String(8), db.ForeignKey('users.id'), primary_key=True)

    user = db.relationship('User', primaryjoin='AuditLogEntry.user_id==User.id')

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(75))
    email = db.Column(db.String(100), unique=True)
    date_created = db.Column(db.DateTime(timezone=True), default=db.func.now())
    can_view_fire_data = db.Column(db.Boolean, default=False)

    def is_authenticated(self):
        return True

    def is_active(self):
        # @todo: crossreference with Google Doc or LDAP.
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

class Action(db.Model):
    __tablename__ = 'actions'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)
    address = db.Column(db.String)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created = db.Column(db.DateTime(timezone=True), default=db.func.now())

    user = db.relationship('User')

class ActivatedAddress(db.Model):
    __tablename__ = 'activated_addresses'

    address = db.Column(db.String, primary_key=True)
