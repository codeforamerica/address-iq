import factory
import factory.alchemy
import factory.fuzzy
import datetime
import pytz
import models

from app import app, db

class FireIncidentFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.FireIncident
        sqlalchemy_session = db.session

    cad_call_number = factory.Sequence(lambda n: n)
    alarm_datetime = factory.fuzzy.FuzzyDateTime(
        datetime.datetime(2013, 1, 1, tzinfo=pytz.utc))


class PoliceIncidentFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.PoliceIncident
        sqlalchemy_session = db.session

    cad_call_number = factory.Sequence(lambda n: "L%d" % n)


class BusinessLicenseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.BusinessLicense
        sqlalchemy_session = db.session

    name = factory.fuzzy.FuzzyText()

class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.User
        sqlalchemy_session = db.session

    email = factory.fuzzy.FuzzyText(suffix='@example.org')
    name = factory.fuzzy.FuzzyText()
    