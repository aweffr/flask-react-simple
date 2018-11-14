#!/usr/bin/env python
# encoding=utf-8


from setuptools import setup

setup(
    name='create-flask-react-app',
    version='0.1.dev',
    packages=['create_flask_react_app'],
    scripts=['bin/cra.py'],
    license='LICENSE.txt',
    long_description=open('README.rst', encoding='utf-8').read(),
    author='aweffr',
    author_email='aweffr@foxmail.com',
    install_requires=[
        "flask>=1.0.0",
    ],
)
