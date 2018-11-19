#!/usr/bin/env python
# encoding=utf-8
import os
from os.path import join as pjoin
from shutil import rmtree
import pathlib
import unittest
import time

from flask import Flask

from flask_reactjs import WebpackDevTask

PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))

admin_page_js_src = """
import React, {Component} from 'react';

class AdminPage extends Component {
  render() {
    return (
      <div>
        AdminPage
      </div>
    );
  }
}

export default AdminPage;
"""

CLEAN = os.environ.get('CLEAN') == "1"


def test_js_files_generator(js_folder):
    with open(pjoin(js_folder, 'global_js.js'), 'w') as f:
        f.writelines('console.log("Hello World");')

    yield 'global_js.js', pjoin(js_folder, 'global_js.js')

    page_dir = pjoin(js_folder, 'pages', 'admin')
    pathlib.Path(page_dir).mkdir(parents=True, exist_ok=True)
    with open(pjoin(page_dir, 'index.js'), 'w') as f:
        f.writelines(admin_page_js_src)

    yield 'admin', pjoin(page_dir, 'index.js')

    page2_dir = pjoin(js_folder, 'pages', 'second')
    pathlib.Path(page2_dir).mkdir(parents=True, exist_ok=True)
    with open(pjoin(page2_dir, 'index.js'), 'w') as f:
        f.writelines('console.log("Hello World From second page");')

    yield "second", pjoin(page2_dir, 'index.js')


class WebpackTest(unittest.TestCase):

    def setUp(self):
        super().setUp()

        self.app = Flask(__name__)
        self.app.config['PROJECT_PATH'] = PROJECT_PATH

        self.webpack = WebpackDevTask(self.app)

        self.js_folder = pjoin(PROJECT_PATH, 'public')

        self.wpconfig_folder = pjoin(PROJECT_PATH, '.webpack_config')
        pathlib.Path(self.wpconfig_folder).mkdir(parents=True, exist_ok=True)

    def test_watcher(self):

        js_folder = self.js_folder

        if os.path.exists(js_folder):
            rmtree(js_folder, ignore_errors=True)
        os.mkdir(js_folder)
        os.mkdir(pjoin(js_folder, 'pages'))

        _iterator = self.webpack._iter_js_entries()
        _file_generater = test_js_files_generator(js_folder)

        f1, generated_file_abs_path = next(_file_generater)
        res1 = next(_iterator)

        self.assertIn(generated_file_abs_path, res1['g'])

        f2, generated_file_abs_path = next(_file_generater)
        res2 = next(_iterator)
        self.assertIn(generated_file_abs_path, res2['pages'])

        f3, generated_file_abs_path = next(_file_generater)
        t1 = time.time()
        res3 = next(_iterator)
        t2 = time.time()

        span = (t2 - t1) * 1000
        self.assertGreaterEqual(span, 500)

        self.assertIn(generated_file_abs_path, res3['pages'])

        print(res1)
        print(res2)
        print(res3)

    def test_generate_config(self):

        # generate files
        for f in test_js_files_generator(self.js_folder):
            pass

        _iterator = self.webpack._iter_js_entries()

        temp = next(_iterator)

        configs = self.webpack.generate_webpack_config(temp)
        for idx, c in enumerate(configs):
            config_file = pjoin(self.wpconfig_folder, 'webpack.config.%d.js' % idx)
            with open(config_file, 'w') as f:
                f.writelines(c)
            self.webpack._run_webpack_from_file(config_file)

    def _clean(self):
        for p in [self.js_folder, self.wpconfig_folder]:
            if os.path.exists(p):
                rmtree(p, ignore_errors=True)

    def tearDown(self):
        super().tearDown()
        if CLEAN:
            print('CLEANING')
            self._clean()
