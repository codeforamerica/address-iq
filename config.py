import os


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    BROWSERID_URL = os.environ['BROWSERID_URL']
    BROWSERID_LOGIN_URL = '/log-in'
    BROWSERID_LOGOUT_URL = '/log-out'

    GOOGLE_PRIVATE_KEY = os.environ['GOOGLE_PRIVATE_KEY'].replace("\\n", "\n")
    GOOGLE_CLIENT_EMAIL = os.environ['GOOGLE_CLIENT_EMAIL']
    GOOGLE_SPREADSHEET_ID = os.environ['GOOGLE_SPREADSHEET_ID']

class ProductionConfig(Config):
    DEBUG = False

class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_ECHO = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

