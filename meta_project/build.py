#!/usr/bin/env python
# encoding=utf-8
import os
import subprocess
import tarfile
import pathlib
import shutil
from glob import glob

P = pathlib.Path


def main():
    ret = subprocess.call('yarn build', shell=True)
    if ret == 0:
        p = P('./build.tar.gz')

        if p.exists():
            os.remove(p)

        with tarfile.open('build.tar.gz', 'x:gz') as tarf:
            tarf.add('./build', arcname='.')
    else:
        print("Build Task Failed!")

    #  build/index.html -> app/templates/index.html
    #  build/static/js -> app/static/js
    #  build/static/css -> app/static/css
    #  build/static/lib -> app/static/lib
    #  build/static/favicon.ico -> app/static/favicon.ico

    p = pathlib.Path('./app')
    if not p.exists():
        p.mkdir()

    p = pathlib.Path('./tmp.tar.gz')
    if p.exists():
        os.remove(p)

    with tarfile.open('tmp.tar', 'x') as tmp:
        tmp.add('./build/static/js', arcname='./app/static/js')
        tmp.add('./build/static/css', arcname='./app/static/css')
        tmp.add('./build/static/lib', arcname='./app/static/lib')
        tmp.add('./build/index.html', arcname='./app/templates/index.html')
        tmp.add('./build/static/favicon.ico', arcname='./app/static/favicon.ico')

    with tarfile.open('tmp.tar', 'r') as tmp:
        for f in tmp:
            try:
                tmp.extract(f)
            except IOError:
                os.remove(f.name)
                tmp.extract(f)
            finally:
                os.chmod(f.name, f.mode)
    print("Copy compiled assets into app folder!")

    shutil.rmtree('./build')
    os.remove('./tmp.tar')


if __name__ == '__main__':
    main()
