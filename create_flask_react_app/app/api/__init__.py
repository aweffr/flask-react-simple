#!/usr/bin/env python
# encoding=utf-8

from flask import Blueprint

bp = Blueprint('api', __name__)

from .routes import *
