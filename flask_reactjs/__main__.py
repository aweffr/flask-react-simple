#!/usr/bin/env python
# encoding=utf-8

import os, sys
import click
import subprocess
import tarfile

import flask_reactjs


@click.command()
@click.option('--install/--no-install', '-I/-N', default=False)
@click.argument('project_name')
def create(project_name, install):
    cwd = os.getcwd()

    dirpath = os.path.join(cwd, project_name)

    if os.path.exists(dirpath):
        print(f'{dirpath} already exists!')
        return

    pkgdir = sys.modules['flask_reactjs'].__path__[0]

    tarf = tarfile.open(os.path.join(pkgdir, 'bundle.tar.gz'))

    tarf.extractall(dirpath)

    if install:
        subprocess.call("yarn install", shell=True, cwd=dirpath)


if __name__ == '__main__':
    create()
