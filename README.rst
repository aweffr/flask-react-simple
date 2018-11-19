======================
Create Flask React App
======================

Introduction
============

1. cra <project_name> Generate a standard flask app with react(Webpack).
2. -N option can be set to avoid yarn install automatically.

约定即配置

public/文件夹里, 根目录下的js文件会被注入到所有模板中, pages/add/index.js的文件会被自动注入到 templates/add.html中


Fetures on the way
==================

1. from flask_reactjs import React - more powerful server rendering
2. code splitting


development
-----------

on Windows:

set FLASK_APP=create_flask_react_app.app:create_app('dev')

set FLASK_DEBUG=1

flask run

on Unix:

Use export instead of set.


Contributors
============

aweffr@foxmail.com
