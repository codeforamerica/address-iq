import unittest
import os

os.environ['APP_SETTINGS'] = 'config.TestingConfig'

from app import app, db, fetch_incidents_at_address


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


import factory
import factory.alchemy
import factory.fuzzy
import models


class FireIncidentFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.FireIncident
        sqlalchemy_session = db.session

    cad_call_number = factory.Sequence(lambda n: n)


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
