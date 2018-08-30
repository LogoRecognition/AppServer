# coding=utf-8
"""Public configuration module."""


class Config(object):
    """Basic configuration class."""

    DEBUG = False
    TESTING = False
    HOST = '0.0.0.0'
    PORT = 8080


class DevelopmentConfig(Config):
    """Used in normal development environment."""

    DEBUG = True


class TestingConfig(Config):
    """Used in testing environment."""

    TESTING = True


config = {
    'development': DevelopmentConfig,
    'test': TestingConfig,
    'default': DevelopmentConfig
}