from app import app, db
import unittest
import os

os.environ['APP_SETTINGS'] = 'config.TestingConfig'

class HomeTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def testHomePageReturns200(self):
        rv = self.app.get('/')

        assert rv.status_code == 200

if __name__ == '__main__':
    unittest.main()
