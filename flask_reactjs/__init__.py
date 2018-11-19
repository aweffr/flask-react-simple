#!/usr/bin/env python
# encoding=utf-8
import os, sys
import subprocess
from collections import defaultdict
from glob import glob
from time import sleep
from os.path import join as pjoin
import pathlib

from shutil import rmtree

from .__main__ import create
from flask import current_app, _app_ctx_stack, Flask

import jinja2


class FlaskReact(object):
    def __init__(self, app=None):
        self.app = app
        self.webpack = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        self.app = app
        self.webpack = WebpackDevTask(app)

    def run_webpack_watcher(self):
        if self.webpack is None:
            raise Exception('Cannot Find the App Instance!')
        self.webpack.run()

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


index_js_template = """
import {{ page_name }} from './{{ page_name }}';

export default {{ page_name }};
"""

react_component_js_template = """
import React, {Component, Fragment} from 'react';

class {{ page_name }} extends Component {
  render() {
    return (
      <div>
        {{ page_name }} page
      </div>
    );
  }
}

export default {{ page_name }};
"""


class WebpackDevTask(object):

    def __init__(self, app: Flask):
        self.app = app
        self.project_path = app.config['PROJECT_PATH']
        self.babel_target_env = app.config.get('BABEL_ENV_TARGET', '> 0.5%, last 2 versions, Firefox ESR, not dead')

        self.watch_dir = os.path.join(self.project_path, 'public')

    def generate_page(self, page_name: str):
        p = pathlib.Path(pjoin(self.project_path, 'public', 'pages', page_name))
        p.mkdir(parents=True, exist_ok=True)

        index_t = jinja2.Template(index_js_template)
        component_t = jinja2.Template(react_component_js_template)

        index_filename = p / 'index.js'
        component_filename = p / (page_name.capitalize() + '.js')

        if not os.path.exists(index_filename) and not os.path.exists(component_filename):
            with open(index_filename, 'w') as f:
                f.writelines(
                    index_t.render(page_name=page_name.capitalize())
                )
            with open(component_filename, 'w') as f:
                f.writelines(
                    component_t.render(page_name=page_name.capitalize())
                )

    def _iter_js_entries(self):
        """
        This iterates over all relevant Javascript files.
        """

        stats = {
            'g': defaultdict(float),
            'pages': defaultdict(float)
        }

        while True:

            out = {
                'g': [],
                'pages': set()
            }

            global_files = glob(os.path.join(self.watch_dir, '*.js'))
            for filename in global_files:
                if os.path.isfile(filename):
                    mtime = os.stat(filename).st_mtime

                    if mtime > stats['g'][filename]:
                        out['g'].append(filename)

                    stats['g'][filename] = mtime

            pages = glob(os.path.join(self.watch_dir, 'pages', '*'))

            for page in pages:
                if os.path.isdir(page):
                    entry_file = os.path.join(page, 'index.js')
                    if not os.path.exists(entry_file):
                        continue

                    page_name = os.path.basename(page)
                    for filename in glob(os.path.join(page, '*')):
                        mtime = os.stat(filename).st_mtime

                        if mtime > stats['pages'][filename]:
                            out['pages'].add(entry_file)

                        stats['pages'][filename] = mtime

            if out['g'] or out['pages']:
                yield out

            sleep(0.5)

    def generate_webpack_config(self, files):

        # Accept output from self._iter_js_entries

        # generate a temp config file for webpack
        # mainly customize the entry and output

        # return a list of webpack files

        template = jinja2.Template("""
const path = require("path");
const webpack = require("webpack");

module.exports = {
  entry: {{ entry_block }},
  mode: "{{ webpack_mode }}", // development or production
  devtool: "cheap-module-source-map",
  module: {
    rules: [
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        loader: "babel-loader",
        options: {
          presets: [
            ["@babel/env", {"targets": "{{ babel_target_env }}"}],
            "@babel/preset-react"
          ],
          plugins: [
            ["@babel/plugin-proposal-class-properties", {loose: true}],
            ["@babel/plugin-proposal-object-rest-spread", {useBuiltIns: true}],
            "@babel/plugin-proposal-optional-chaining",
          ]
        }
      },
      {
        test: /\.css$/,
        use: ["style-loader", "css-loader"]
      }
    ]
  },
  resolve: {extensions: ["*", ".js", ".jsx"]},
  output: {
    path: {{ output_dir }},

    // the target directory for all output files
    filename: "{{ output_filename }}",
  }
};
""")

        assert isinstance(files, dict)

        if self.app.debug or self.app.testing:
            webpack_mode = 'development'
        else:
            webpack_mode = 'production'

        out = []

        for global_js in files['g']:
            filename = os.path.basename(global_js)

            config = template.render(
                webpack_mode=webpack_mode,
                entry_block=f"path.resolve('public/', '{filename}')",
                output_dir=f"path.resolve('.', 'app/static/dist')",
                output_filename=filename,
                babel_target_env=self.babel_target_env
            )
            out.append(config)

        for page_js in files['pages']:
            dir_name = os.path.basename(os.path.dirname(page_js))

            config = template.render(
                webpack_mode=webpack_mode,
                entry_block=f"path.resolve('public/', 'pages/{dir_name}/index.js')",
                output_dir=f"path.resolve('.', 'app/static/dist/{dir_name}')",
                output_filename='index.js',
                babel_target_env=self.babel_target_env
            )
            out.append(config)

        return out

    def _run_webpack_from_file(self, config_path):

        cmd = f"yarn run webpack --config {config_path}"
        print('cmd to run:', cmd)

        p = subprocess.call(cmd, shell=True, cwd=self.project_path)

    def run(self):
        _iter = self._iter_js_entries()

        temp_webpack_dir = pathlib.Path(pjoin(self.project_path, '.webpack_config'))
        temp_webpack_dir.mkdir(parents=True, exist_ok=True)

        for batch in _iter:
            configs = self.generate_webpack_config(batch)
            for idx, config in enumerate(configs):
                config_file = pjoin(temp_webpack_dir, 'webpack.config.%d.js' % idx)

                with open(config_file, 'w') as f:
                    f.writelines(config)

                self._run_webpack_from_file(config_file)
