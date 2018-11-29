#!/usr/bin/env python
# encoding=utf-8
import os
import subprocess
import tarfile
import pathlib, shutil
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

    # ↓↓↓当./app存在时拷贝进去
    # 1. 拷贝 build/index.html 到 app/templates
    # 2. 拷贝 build/static/js 到 app/static/js
    # 3. 拷贝 build/static/css 到 app/static/css
    # 3. 拷贝 build/static/lib 到 app/static/lib
    # 4. 拷贝 build/static/favicon.ico 到 app/static/favicon.ico

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
