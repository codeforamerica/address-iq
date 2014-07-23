from app import db

#class FireIncident(db.Model):
#    __tablename__ = 'fire_incidents'

#class FireDispatch(db.Model):
#    __tablename__ = 'fire_dispatches'
#    pass

#class PoliceIncident(db.Model):
#    __tablename__ = 'police_incidents'
#    pass

class BusinessLicense(db.Model):
    __tablename__ = 'all_business_licenses'
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column('name', db.String(200))
    business_class = db.Column('business_class', db.String(40))
    business_service_description = db.Column('business_service_description', db.String(100))
    business_product = db.Column('business_product', db.String(40))
    business_address = db.Column('business_address', db.String(200))
    business_zip = db.Column('business_zip', db.String(20))
