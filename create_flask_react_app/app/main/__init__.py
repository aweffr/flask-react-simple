#!/usr/bin/env python
# encoding=utf-8

from flask import Blueprint

bp = Blueprint('main', __name__)

from .routes import *