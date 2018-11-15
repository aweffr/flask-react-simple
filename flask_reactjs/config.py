#!/usr/bin/env python
# encoding=utf-8
import os
import secrets


class Config(object):
    ENV = 'production'


class DevConfig(Config):
    ENV = 'development'
    SECRET_KEY = 'happy'


class TestConfig(Config):
    TESTING = True
    SECRET_KEY = 'test_secret_key'


class ProdConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY') or secrets.token_urlsafe(24)


_configs = {
    'dev': DevConfig,
    'test': TestConfig,
    'production': ProdConfig
}


def get_config(_id):
    assert _id in _configs, f"Supported _id: {' '.join(_configs)}"
    return _configs[_id]
