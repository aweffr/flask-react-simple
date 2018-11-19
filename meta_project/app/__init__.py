#!/usr/bin/env python
# encoding=utf-8

from flask import Flask


# Init flask_login, flask-sqlalchemy, pymongo, etc...


def create_app(config_obj):
    app = Flask(__name__)
    app.config.from_object(config_obj)

    # Region: XXX.init_app(app)

    # Region: register_blueprint
    from .api import bp
    app.register_blueprint(bp, url_prefix='/api')

    from .main import bp
    app.register_blueprint(bp)

    return app
