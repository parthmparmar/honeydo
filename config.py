class Config(object):
    DEBUG = False
    TESTING = False
    #DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):

    DEBUG = False

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI='postgresql://postgres:2123@localhost/honeydo'
    DEBUG = True
    SECRET_KEY = 'thisisthesecretkey'

class TestingConfig(Config):
    TESTING = True
