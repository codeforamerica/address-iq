import os


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ['SECRET_KEY']
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_BINDS = {
        'lbc_data': os.environ['DATABASE_URL']
    }
    BROWSERID_URL = os.environ['BROWSERID_URL']
    BROWSERID_LOGIN_URL = '/log-in'
    BROWSERID_LOGOUT_URL = '/log-out'

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_BINDS = {
        'lbc_data': os.environ.get('DATA_DATABASE_URL')
    }

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
    SQLALCHEMY_BINDS = {
        'lbc_data': 'sqlite:///:memory:'
    }

