#!/usr/bin/env python
# encoding=utf-8

from flask import jsonify
from . import bp
from .data import Data


@bp.route('/users')
def users():
    return jsonify(Data.users())


@bp.route('/todos')
def todos():
    return jsonify(Data.todos())
