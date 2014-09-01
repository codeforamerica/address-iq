from selenium import webdriver
from selenium.webdriver.support.ui import Select

from flask import Flask, render_template, abort, request, Response, session, redirect, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, login_user, logout_user, current_user, login_required

import unittest
import os
from browserid import BrowserID
import requests
import time

remote_browser = False
if os.environ.get('NOTIFY_TEST_REMOTE_BROWSER') == "YES":
    remote_browser = True

SAUCE_USERNAME = os.environ.get('SAUCE_USERNAME')
SAUCE_ACCESS_KEY = os.environ.get('SAUCE_ACCESS_KEY')

using_travis = False
hub_url = "%s:%s@localhost:4445" % (SAUCE_USERNAME, SAUCE_ACCESS_KEY)

if 'TRAVIS_JOB_NUMBER' in os.environ:
    using_travis = True
    hub_url = "%s:%s@ondemand.saucelabs.com:80" % (SAUCE_USERNAME, SAUCE_ACCESS_KEY)
    print "USING TRAVIS", hub_url

from app import app, db
import models
from models import FireIncident, PoliceIncident, User
from factories import FireIncidentFactory, PoliceIncidentFactory, BusinessLicenseFactory
import datetime
import pytz


def generate_test_data():

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

def generate_persona_credentials():
    response = requests.get('http://personatestuser.org/email')
    json = response.json()
    email = json['email']
    password = json['pass']
    return dict(email=email, password=password)

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
    # @todo: When we incorporate LDAP, update this to pull real name.
    name = 'Fireworks Joe'
    user = models.User.query.filter(models.User.email==email).first()
    if not user:
        user = create_user(name, email)

    return user

def log_in(browser, persona_user):
    browser.get('http://localhost:5000')
    browser.implicitly_wait(3)

    login_link = browser.find_element_by_link_text('Log in')
    login_link.click()

    browser_id = BrowserID(browser)
    browser_id.sign_in(persona_user['email'], persona_user['password'])


class AddressPageTest(unittest.TestCase):

    def setUp(self):
        generate_test_data()
        db.session.commit()

        self.persona_user = generate_persona_credentials()

        if remote_browser:
            caps = webdriver.DesiredCapabilities.INTERNETEXPLORER
            caps['platform'] = "Windows XP"
            caps['version'] = "8"
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

    def test_user_can_log_in_and_log_out(self):
        self.browser.get('http://localhost:5000')
        self.browser.implicitly_wait(3)

        # On the homepage, the user sees the 'Log in' link.
        login_link = self.browser.find_element_by_link_text('Log in')
        self.assertTrue(login_link.is_displayed())

        # The user is then able to actually log in.
        login_link.click()

        browser_id = BrowserID(self.browser)
        browser_id.sign_in(self.persona_user['email'], self.persona_user['password'])

        time.sleep(5)
        logout_link = self.browser.find_element_by_link_text('Log out')
        self.assertTrue(logout_link.is_displayed())

        # The user can click the logout link and again see the login link.
        logout_link.click()
        login_link = self.browser.find_element_by_link_text('Log in')
        self.assertTrue(login_link.is_displayed())

    def test_user_can_log_out(self):
        # @todo: Test that limitations on what they can see are working.

        return True

    def test_page_loads_and_shows_top_fire_calls_for_year(self):
        log_in(self.browser, self.persona_user)
        self.browser.implicitly_wait(3)

        time.sleep(5)
        self.browser.get('http://localhost:5000/address/123 test ln')

        call_types_list = self.browser.find_element_by_class_name("call-types")
        self.assertTrue(call_types_list.is_displayed())
        self.assertIn('Lung Fell Off', call_types_list.text)

    def test_changing_to_police_shows_top_police_calls_for_year(self):
        log_in(self.browser, self.persona_user)

        time.sleep(5)
        self.browser.get('http://localhost:5000/address/123 test ln')

        police_tab = self.browser.find_element_by_id('tab-police')
        police_tab.click()

        self.assertIn('active', police_tab.get_attribute('class'))

        call_types_list = self.browser.find_element_by_class_name("call-types")
        self.assertTrue(call_types_list.is_displayed())
        self.assertIn("Runnin' With The Devil", call_types_list.text)

    def test_changing_date_range_changes_displayed_data(self):
        log_in(self.browser, self.persona_user)

        time.sleep(5)
        self.browser.get('http://localhost:5000/address/123 test ln')

        select = Select(self.browser.find_element_by_id('data-date-range'))
        select.select_by_value("7")

        call_types_list = self.browser.find_element_by_class_name("call-types")
        self.assertTrue(call_types_list.is_displayed())
        self.assertNotIn('Lung Fell Off', call_types_list.text)

if __name__ == '__main__':
    unittest.main()
