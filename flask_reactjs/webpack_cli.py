#!/usr/bin/env python
# encoding=utf-8

import click
from flask.cli import with_appcontext


@click.group()
def wp():
    """Perform webpack operations"""
    pass


@wp.command()
@with_appcontext
def watch():
    from . import WebpackDevTask
