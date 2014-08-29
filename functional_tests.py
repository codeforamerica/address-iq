from selenium import webdriver
from selenium.webdriver.support.ui import Select

import unittest

import os

remote_browser = False
if os.environ.get('NOTIFY_TEST_REMOTE_BROWSER') == "YES":
    remote_browser = True

SAUCE_USERNAME = os.environ.get('SAUCE_USERNAME')
SAUCE_ACCESS_KEY = os.environ.get('SAUCE_ACCESS_KEY')

using_travis = False
hub_url = "%s:%s@localhost:4445" % (SAUCE_USERNAME, SAUCE_ACCESS_KEY)

if 'TRAVIS_JOB_NUMBER' in os.environ:
    using_travis = True
    print "USING TRAVIS", hub_url

from app import app, db
from models import FireIncident, PoliceIncident
from factories import FireIncidentFactory, PoliceIncidentFactory, BusinessLicenseFactory
import datetime


def generate_test_data():
    db.create_all()

    def get_date_days_ago(days):
        return datetime.datetime.now() - datetime.timedelta(days=days)

    [FireIncidentFactory(incident_address="123 TEST LN",
                         alarm_datetime=get_date_days_ago(5),
                         actual_nfirs_incident_type_description="Broken Nose")
     for i in range(0, 5)]
    [FireIncidentFactory(incident_address="123 TEST LN",
                         alarm_datetime=get_date_days_ago(20),
                         actual_nfirs_incident_type_description="Stubbed Toe")
     for i in range(0, 8)]
    [FireIncidentFactory(incident_address="123 TEST LN",
                         alarm_datetime=get_date_days_ago(40),
                         actual_nfirs_incident_type_description="Myocardial Infarction")
     for i in range(0, 7)]
    [FireIncidentFactory(incident_address="123 TEST LN",
                         alarm_datetime=get_date_days_ago(200),
                         actual_nfirs_incident_type_description="Lung Fell Off")
     for i in range(0, 10)]

    [PoliceIncidentFactory(incident_address="123 TEST LN",
                           call_datetime=get_date_days_ago(5),
                           final_cad_call_type_description="Stepped on a Crack")
     for i in range(0, 3)]
    [PoliceIncidentFactory(incident_address="123 TEST LN",
                           call_datetime=get_date_days_ago(20),
                           final_cad_call_type_description="Whipped It")
     for i in range(0, 8)]
    [PoliceIncidentFactory(incident_address="123 TEST LN",
                           call_datetime=get_date_days_ago(40),
                           final_cad_call_type_description="Safety Dance")
     for i in range(0, 9)]
    [PoliceIncidentFactory(incident_address="123 TEST LN",
                           call_datetime=get_date_days_ago(200),
                           final_cad_call_type_description="Runnin' With The Devil")
     for i in range(0, 6)]

def remove_test_data():
    db.session.query(FireIncident).filter(FireIncident.incident_address=="123 TEST LN").delete()
    db.session.query(PoliceIncident).filter(PoliceIncident.incident_address=="123 TEST LN").delete()

class AddressPageTest(unittest.TestCase):

    def setUp(self):
        generate_test_data()
        db.session.commit()

        if remote_browser:
            caps = webdriver.DesiredCapabilities.INTERNETEXPLORER
            caps['platform'] = "Windows XP"
            caps['version'] = "7"
            if using_travis:
                caps['tunnel-identifier'] = os.environ['TRAVIS_JOB_NUMBER']
                print caps
            self.browser = webdriver.Remote(
                command_executor='http://%s/wd/hub' % hub_url,
                desired_capabilities=caps)
        else:
            self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)


    def tearDown(self):
        remove_test_data()
        db.session.commit()
        self.browser.quit()

    def test_page_loads_and_shows_top_fire_calls_for_year(self):
        self.browser.get('http://localhost:5000/address/123 test ln')

        call_types_list = self.browser.find_element_by_class_name("call-types")
        self.assertTrue(call_types_list.is_displayed())
        self.assertIn('Lung Fell Off', call_types_list.text)

    def test_changing_to_police_shows_top_fire_calls_for_police(self):
        self.browser.get('http://localhost:5000/address/123 test ln')

        police_tab = self.browser.find_element_by_id('tab-police')
        police_tab.click()

        self.assertIn('active', police_tab.get_attribute('class'))

        call_types_list = self.browser.find_element_by_class_name("call-types")
        self.assertTrue(call_types_list.is_displayed())
        self.assertIn("Runnin' With The Devil", call_types_list.text)

    def test_changing_date_range_changes_displayed_data(self):
        self.browser.get('http://localhost:5000/address/123 test ln')

        select = Select(self.browser.find_element_by_id('data-date-range'))
        select.select_by_value("7")

        call_types_list = self.browser.find_element_by_class_name("call-types")
        self.assertTrue(call_types_list.is_displayed())
        self.assertNotIn('Lung Fell Off', call_types_list.text)

if __name__ == '__main__':
    unittest.main()
