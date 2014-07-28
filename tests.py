import unittest
import os
import datetime

os.environ['APP_SETTINGS'] = 'config.TestingConfig'

from app import app, db
from app import fetch_incidents_at_address, count_incidents_by_timeframes


class HomeTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def testHomePageReturns200(self):
        rv = self.app.get('/')

        assert rv.status_code == 200


class AddressUtilityTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def test_fetch_incidents_at_address_returns_all_empty_types(self):

        incidents = fetch_incidents_at_address("123 main st")

        assert 'fire' in incidents
        assert 'police' in incidents
        assert 'businesses' in incidents

        assert len(incidents['fire']) == 0
        assert len(incidents['police']) == 0
        assert len(incidents['businesses']) == 0

    def test_fetch_incident_at_address_returns_correct_number_of_items(self):
        [FireIncidentFactory(incident_address="123 MAIN ST")
         for i in range(5)]
        [PoliceIncidentFactory(incident_address="123 MAIN ST")
         for i in range(3)]
        [BusinessLicenseFactory(business_address="123 MAIN ST")
         for i in range(1)]

        db.session.flush()

        incidents = fetch_incidents_at_address("123 MAIN ST")
        assert len(incidents['fire']) == 5
        assert len(incidents['police']) == 3
        assert len(incidents['businesses']) == 1

    def test_fetch_incident_at_address_works_if_lowercase_supplied(self):
        [FireIncidentFactory(incident_address="123 MAIN ST")
         for i in range(0, 5)]
        [PoliceIncidentFactory(incident_address="123 MAIN ST")
         for i in range(0, 3)]
        [BusinessLicenseFactory(business_address="123 MAIN ST")
         for i in range(0, 1)]

        db.session.flush()

        incidents = fetch_incidents_at_address("123 main st")
        assert len(incidents['fire']) == 5
        assert len(incidents['police']) == 3
        assert len(incidents['businesses']) == 1
        pass

    def test_count_incidents_returns_proper_counts_for_default_days(self):
        def get_date_days_ago(days):
            return datetime.datetime.now() - datetime.timedelta(days=days)

        [FireIncidentFactory(incident_address="123 MAIN ST",
                             alarm_datetime=get_date_days_ago(5))
         for i in range(0, 5)]
        [FireIncidentFactory(incident_address="123 MAIN ST",
                             alarm_datetime=get_date_days_ago(20))
         for i in range(0, 8)]
        [FireIncidentFactory(incident_address="123 MAIN ST",
                             alarm_datetime=get_date_days_ago(40))
         for i in range(0, 7)]
        [FireIncidentFactory(incident_address="123 MAIN ST",
                             alarm_datetime=get_date_days_ago(200))
         for i in range(0, 10)]

        [PoliceIncidentFactory(incident_address="123 MAIN ST",
                               call_datetime=get_date_days_ago(5))
         for i in range(0, 3)]
        [PoliceIncidentFactory(incident_address="123 MAIN ST",
                               call_datetime=get_date_days_ago(20))
         for i in range(0, 8)]
        [PoliceIncidentFactory(incident_address="123 MAIN ST",
                               call_datetime=get_date_days_ago(40))
         for i in range(0, 9)]
        [PoliceIncidentFactory(incident_address="123 MAIN ST",
                               call_datetime=get_date_days_ago(200))
         for i in range(0, 6)]

        db.session.flush()

        incidents = fetch_incidents_at_address("123 main st")
        counts = count_incidents_by_timeframes(incidents, [7, 30, 90, 365])

        assert counts['fire'][7] == 5
        assert counts['fire'][30] == 13
        assert counts['fire'][90] == 20
        assert counts['fire'][365] == 30

        assert counts['police'][7] == 3
        assert counts['police'][30] == 11
        assert counts['police'][90] == 20
        assert counts['police'][365] == 26

    def test_count_incidents_returns_zeros_when_no_incidents(self):
        import datetime

        def get_date_days_ago(days):
            return datetime.datetime.now() - datetime.timedelta(days=days)

        incidents = fetch_incidents_at_address("123 main st")
        counts = count_incidents_by_timeframes(incidents, [7, 30, 90, 365])

        assert counts['fire'][7] == 0
        assert counts['fire'][30] == 0
        assert counts['fire'][90] == 0
        assert counts['fire'][365] == 0

        assert counts['police'][7] == 0
        assert counts['police'][30] == 0
        assert counts['police'][90] == 0
        assert counts['police'][365] == 0

    def test_address_page_with_incidents_returns_200(self):
        [FireIncidentFactory(incident_address="123 MAIN ST")
         for i in range(0, 5)]

        db.session.flush()

        rv = self.app.get('/address/123 main st')
        assert rv.status_code == 200

    def test_address_page_with_no_incidents_returns_404(self):
        rv = self.app.get('/address/123 main st')
        assert rv.status_code == 404

import factory
import factory.alchemy
import factory.fuzzy
import pytz
import models


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

if __name__ == '__main__':
    unittest.main()
