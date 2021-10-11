import os

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SECRET_KEY = 'v5d&fiouf3pwht^^2ja5r!q7ex3e)294dj)xr%668e5845^)oz'
    DB_USERNAME = 'pi'
    DB_HOSTNAME = os.environ.get('DATABASE_URL', '197.255.121.22')
    DB_PASSWORD = 'aduuna14'
    DB_NAME = 'ejuma'

class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class TestingConfig(Config):
    TESTING = True
