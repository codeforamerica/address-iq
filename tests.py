import unittest
import os

os.environ['APP_SETTINGS'] = 'config.TestingConfig'

from app import app, db, fetch_incidents_at_address

print db.engine

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
        x = [FireIncidentFactory(incident_address="123 MAIN ST") for i in range(0, 5)]
        db.session.flush()

        incidents = fetch_incidents_at_address("123 MAIN ST")
        assert len(incidents['fire']) == 5
        assert len(incidents['police']) == 0
        assert len(incidents['businesses']) == 0

    def test_fetch_incident_at_address_works_if_lowercase_supplied(self):
        x = [FireIncidentFactory(incident_address="123 MAIN ST") for i in range(0, 5)]
        db.session.flush()

        incidents = fetch_incidents_at_address("123 main st")
        assert len(incidents['fire']) == 5
        assert len(incidents['police']) == 0
        assert len(incidents['businesses']) == 0

import factory, factory.alchemy
import models

class FireIncidentFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = models.FireIncident
        sqlalchemy_session = db.session

    cad_call_number = factory.Sequence(lambda n: n)



if __name__ == '__main__':
    unittest.main()
