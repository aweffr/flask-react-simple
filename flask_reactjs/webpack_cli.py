#!/usr/bin/env python
# encoding=utf-8

import click
from flask import current_app
from flask.cli import with_appcontext


@click.group()
def wp():
    """Perform webpack operations"""
    pass


@wp.command()
@with_appcontext
def watch():
    from . import WebpackDevTask
    webpack = WebpackDevTask(current_app)
    webpack.run()


@wp.command()
@click.argument('page_name')
@with_appcontext
def gen_page(page_name):
    from . import WebpackDevTask
    webpack = WebpackDevTask(current_app)
    webpack.generate_page(page_name)
