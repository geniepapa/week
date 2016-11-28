import os
basedir = os.path.abspath(os.path.dirname(__file__))
print basedir


class Config:

    SECRET_KEY = 'geniepapa@gmail.com'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///'+os.path.join(basedir, 'data.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    pass

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig
}

