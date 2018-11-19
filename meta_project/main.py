#!/usr/bin/env python
# encoding=utf-8

from config import get_config
from app import create_app

DevConfig = get_config('dev')

app = create_app(DevConfig)

if __name__ == '__main__':
    app.run(threaded=True)
