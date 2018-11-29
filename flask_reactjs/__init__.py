#!/usr/bin/env python
# encoding=utf-8
import os, sys
import subprocess
import click
import tarfile
import pathlib, shutil


@click.command()
@click.argument('project_name')
def create(project_name):
    cwd = os.getcwd()

    dst = pathlib.Path(cwd) / project_name

    if dst.exists():
        print(f'{dst} already exists! Return!')
        return

    ret = subprocess.call(f"create-react-app {project_name}", cwd=cwd, shell=True)
    if ret != 0:
        print("you need to globally install create-react-app first!")
        return

    # adjust dst/public layout
    public_folder = dst / 'public'
    p = public_folder / 'static' / 'lib'
    p.mkdir(parents=True)

    shutil.move(public_folder / 'favicon.ico', public_folder / 'static' / 'favicon.ico')

    lines = []
    with open(public_folder / "index.html", "r") as f:
        for line in f:
            line = line.replace("%PUBLIC_URL%/favicon.ico", "%PUBLIC_URL%/static/favicon.ico")
            lines.append(line)

    with open(public_folder / "index.html", "w") as f:
        f.writelines("".join(lines))

    # Copy python files
    pkg_dir = sys.modules['flask_reactjs'].__path__[0]

    tar_f = tarfile.open(os.path.join(pkg_dir, 'bundle.tar.gz'))

    tar_f.extractall(dst)

    print("Cloning venv...")
    ret = subprocess.call(f"{sys.executable} -m venv venv", cwd=dst, shell=True)
    if ret == 0:
        print("Cloning venv finish!")
    else:
        print("Cloning venv failed! :(")
        return

    if sys.platform.startswith('win'):
        venv_executable = os.path.join(dst, "venv", "Scripts", "python.exe")
    elif sys.platform.startswith('linux'):
        venv_executable = os.path.join(dst, "venv", "bin", "python.exe")
    else:
        raise Exception(f"Not Supported Platform: {sys.platform}; Please install flask by yourself!")

    subprocess.call(f"{venv_executable} -m pip install flask")

    print("Cra complete! Happy Hacking!")
