import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = '\x08\x91[\x91.\xe08\x10\xa2\x05{\xe7\x979\x87\x0bI\x04\x19\x84\x08\x19\x19\x08'
    JWT_SECRET_KEY = '\x08\x91[\x91.\xe08\x10\xa2\x05{\xe7\x979\x87\x0bI\x04\x19\x84\x08\x19\x19\x08'
    SQLALCHEMY_DATABASE_URI = "postgresql://handsdown:handsdown@localhost/handsdown_dev"
    THREADED = True
    POSTS_PER_PAGE = 3


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
