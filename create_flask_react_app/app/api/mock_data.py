#!/usr/bin/env python
# encoding=utf-8

import json
from urllib.request import urlopen


class Data(object):
    _todos = None

    _users = None

    @classmethod
    def todos(cls):
        if cls._todos is None:
            fd = urlopen('https://jsonplaceholder.typicode.com/todos')
            cls._todos = json.load(fd)
        return cls._todos

    @classmethod
    def users(cls):
        if cls._users is None:
            fd = urlopen('https://jsonplaceholder.typicode.com/users')
            cls._users = json.load(fd)
        return cls._users
