class Config(object):
    DEBUG = False
    TESTING = False
    #DATABASE_URI = 'sqlite:///:memory:'

class ProductionConfig(Config):
    #SQLALCHEMY_DATABASE_URI='postgresql://[postgres]:[2123]@localhost/[dbName]'
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
