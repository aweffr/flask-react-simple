#!/usr/bin/env python
# encoding=utf-8

from flask import Flask
from ..config import get_config


# Init flask_login, flask-sqlalchemy, pymongo, etc...


def create_app(_id='dev'):
    app = Flask(__name__)
    app.config.from_object(get_config(_id))

    # Region: XXX.init_app(app)

    # Region: register_blueprint
    from .api import bp
    app.register_blueprint(bp, url_prefix='/api')

    from .main import bp
    app.register_blueprint(bp)

    return app
