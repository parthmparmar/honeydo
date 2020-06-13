import os
from dotenv import load_dotenv
import psycopg2

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
        DATABASE_URL = os.getenv('DATABASE_URL')
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        DEBUG = False

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:2123@localhost/honeydo'
    DEBUG = True
    SECRET_KEY = 'thisisthesecretkey'
    def devDB():
        return SQLALCHEMY_DATABASE_URI

class TestingConfig(Config):
    TESTING = True
