import os
from dotenv import load_dotenv

class Config(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    TESTING = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.getenv('EMAIL_USER')
    MAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')

if os.getenv('SECRET_KEY'):
    class ProductionConfig(Config):
        SECRET_KEY = os.getenv('SECRET_KEY')
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
        DEBUG = False

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:2123@localhost/honeydo'
    DEBUG = True
    SECRET_KEY = 'thisisthesecretkey'
    def devDB():
        return SQLALCHEMY_DATABASE_URI

class TestingConfig(Config):
    TESTING = True
