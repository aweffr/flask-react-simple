#!/usr/bin/env python
# encoding=utf-8

from .__main__ import create
from flask import current_app, _app_ctx_stack


class FlaskReact(object):
    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        app.config.setdefault('BABEL_ENV_TARGET', '> 0.5%, last 2 versions, Firefox ESR, not dead')

    def inject_page_source(self):
        raise NotImplemented

    def teardown(self):
        ctx = _app_ctx_stack.top
        if hasattr(ctx, 'react'):
            # Do clean staff
            ctx.react = None

    @property
    def sources(self):
        ctx = _app_ctx_stack.top
        if ctx is not None:
            if not hasattr(ctx, 'react'):
                ctx.react = {
                    'sources': ['1.js', '2.js']
                }
            return ctx.react['sources']
