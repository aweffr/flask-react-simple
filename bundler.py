#!/usr/bin/env python
# encoding=utf-8
import os
import re
import tarfile
import glob

base_dir = os.path.dirname(__file__)
filename = os.path.join(base_dir, 'flask_reactjs', 'bundle.tar.gz')

src_dir = os.path.join(base_dir, 'meta_project')

black_list = [
    'node_modules',
    'yarn.lock',
    'venv',
    '__pycache__'
]


def need_exclude(filename):
    for name in black_list:
        if name in filename:
            return True
        if 'public' in filename and 'pages' in filename:
            return True
    return False


def bundler():
    files_to_add = []
    for f in glob.glob(src_dir + '/*'):
        if need_exclude(f):
            continue
        files_to_add.append(f)

    with tarfile.open(filename, 'w:gz') as tarf:
        for f in files_to_add:
            arc_name = f.replace(src_dir, '.')
            print(arc_name)
            tarf.add(f, arc_name, exclude=need_exclude)


if __name__ == '__main__':
    bundler()
