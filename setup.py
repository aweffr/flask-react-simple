#!/usr/bin/env python
# encoding=utf-8

import sys

from setuptools import setup

if 'sdist' in sys.argv:
    from bundler import bundler

    bundler()

setup(
    name='flask-react-simple',
    version='0.1.4',
    packages=['flask_reactjs'],
    license='LICENSE.txt',
    long_description=open('README.rst', encoding='utf-8').read(),
    author='aweffr',
    author_email='aweffr@foxmail.com',
    url='https://github.com/aweffr/flask-react-simple',
    python_requires='>=3.6',
    include_package_data=True,  # specify data files to be included in your packages
    install_requires=[
        "flask>=1.0.2",
        "click>=7.0"
    ],
    entry_points={
        'console_scripts': [
            'cra = flask_reactjs:create'
        ],
        'flask.commands': [
            "wp = flask_reactjs.webpack_cli:wp"
        ],
    }
)
