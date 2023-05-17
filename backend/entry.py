#!/usr/bin/env python3
"""
    Entry point to configuration in the backend server
    The sole purpose of this file is to ensure that
    the environment is ready to run the configuration file
    conf.py

"""

from funcs import *

from pathlib import Path
import subprocess
import sys


pre_apt_packages = ['ufw', 'python3-pip', 'libsystemd-dev']
for package in pre_apt_packages:
    if not check_apt_pkg(package):
        @set_root_and_run
        def install_apt_pkg():
            print(f"Authenticate to install {package}")
            print(f"Installing {package}...")
            return ["apt-get", "install", package]
        install_apt_pkg()
    else:
        print(f"{package} already installed")

pre_pip_packages = ['systemd']
for package in pre_pip_packages:
    if not check_pkg(package):
        install_pkg(package)
    else:
        print(f"{package} already installed")

# Copy all files the end with *.py to
# the directory /home/achira/myproject

src_dir_achira = "/home/achira/Desktop/achira/Desktop/configuration/backend"
src_dir_guest = f"/home/{user()}/configuration"
dest_dir = f"/home/{user()}/myproject"
dir = src_dir_achira if user() == "achira" else src_dir_guest

files = []
print(f"Copying files from {dir} to {dest_dir}...")
for file in Path(dir).glob("*.py"):
    files.append(file)
    copy_file(file, dest_dir)


# Run the conf.py in myproject
os.chdir(dest_dir)
print(cwd())

print(sys.executable)

# Activate the environment in myproject
activate_script = "bin/activate"
print(activate_script)

activate_command = str(Path('myprojectenv').resolve() / activate_script)
print(activate_command)

@set_root_and_run
def activate_env():
    subprocess.run(activate_command, shell=True)

activate_env()


files_to_remove = os.listdir(dest_dir)
for file in files:
    if file.name in files_to_remove:
        print(f"Removing {file.name}...")
        os.remove(f"{dest_dir}/{file.name}")





# My name is Achira
# I am a software engineer
# I am a full stack engineer

# If you are using this file ensure that
# you have funcs.py and conf.py in the same directory