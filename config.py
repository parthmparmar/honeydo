import os

class Config(object):
    DEBUG = False
    TESTING = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('EMAIL_USER')
    MAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')

class ProductionConfig(Config):

    DEBUG = False

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:2123@localhost/honeydo'
    DEBUG = True
    SECRET_KEY = 'thisisthesecretkey'
    def devDB():
        return SQLALCHEMY_DATABASE_URI

class TestingConfig(Config):
    TESTING = True
