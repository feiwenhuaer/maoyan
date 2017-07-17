"""
This file includes all of the  common setting
Just like Debug、Template and so on

Important: Your param's name must be the upper case.otherwise it will not be included by flask

"""
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    CACHE_TYPE = "memcached"

    @staticmethod
    def init_app(app):
        pass


class DevelopConfig(Config):
    # Open Debug mode
    DEBUG = True


class ProductConfig(Config):

    @staticmethod
    def init_app(app):
        Config.init_app(app)
        pass


# Choose config by str
config = {
    'dev': DevelopConfig,
    'pro': ProductConfig,
}
