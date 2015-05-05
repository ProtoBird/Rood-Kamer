# -*- coding: utf-8 -*-
import os

os_env = os.environ


class Config(object):
    SECRET_KEY = os_env.get('RK_SKI', 'secret-key')  # TODO: Change me
    RK_ADMIN = os_env.get('RK_ADMIN')
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    BCRYPT_LOG_ROUNDS = 13
    ASSETS_DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.


class ProdConfig(Config):
    """Production configuration."""
    ENV = 'prod'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/example'  # TODO: Change
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar


class DevConfig(Config):
    """Development configuration."""
    ENV = 'dev'
    DEBUG = True

    SQLALCHEMY_ECHO = False
    DEBUG_TB_ENABLED = True
    ASSETS_DEBUG = True  # Don't bundle/minify static assets
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.

    RK_DB = os_env.get('RK_DB')
    RK_DB_PASSWORD = os_env.get('RK_DB_PASSWORD')
    RK_DB_HOST = 'localhost'

    SQLALCHEMY_DATABASE_URI = "mysql://%s:%s@%s:3306/%s" % (Config.RK_ADMIN,
                                                            RK_DB_PASSWORD,
                                                            RK_DB_HOST,
                                                            RK_DB)


class TestConfig(Config):
    """Testing configuration"""

    DB_NAME = "test.db"
    SQLALCHEMY_DATABASE_URI = "sqlite://"
    TESTING = True
    DEBUG = True
    BCRYPT_LOG_ROUNDS = 1  # For faster tests
    WTF_CSRF_ENABLED = False  # Allows form testing
    PRESERVE_CONTEXT_ON_EXCEPTION = False
