#!/usr/bin/env python3
"""Some configuration on web01"""
from functools import wraps
import getpass
import os
from pathlib import Path
import pkg_resources
import shutil
import socket
import subprocess

packages = ['virtualenv', 'numpy']

def check_pkg(pkg_name):
    try:
        pkg_resources.get_distribution(pkg_name)
        print(f"{pkg_name} resource was found.")
        return True

    except pkg_resources.DistributionNotFound:
        return False

def install_pkg(pkg_name):
    if subprocess.check_call(['pip3', 'install', pkg_name]) == 0:
        print(pkg_name + "installed successfuly")

    else:
        print("An error was encountered during the installation process")

def is_port_open(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        if result == 0:
            print(f"host={host!r}, port={port!r} is listening")
            return True

        else:
            return False

    except socket.error:
        return False

    finally:
        sock.close()

def copy_file(src, dst):
    try:
        shutil.copy2(src, dst)
        print(f"Copied {src} to {dst} as successifully!")
        return 0

    except IOError as e:
        print("An error occured during the process")
        return 1

def set_root_and_run(run_instance):
    @wraps(run_instance)
    def wrapper_function(*args, **kwargs):
        current_user = user()

        with subprocess.Popen(
            ['sudo', '-S'] + run_instance(*args, **kwargs),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        ) as process:
            process.communicate(input=f"{getpass.getpass()}\n".encode())
            output = process.communicate()[0].decode()

        print(output)

    return wrapper_function()
                


host = lambda: socket.gethostname()
user = lambda: getpass.getuser()
run_process = lambda args: subprocess.check_call(args, shell=True)
root = lambda: os.geteuid() == 0

class Stack:
    stack = []

    def add_to_stack(self, value):
        self.stack.append(value)

    def read_stack(self):
        return self.stack.pop()

stack = Stack()

for i in packages:
    if check_pkg(i):
        continue
    else:
        install_pkg(i)

path = os.chdir(Path.home())
dirs = os.listdir(path)

if "myproject" not in dirs:
    os.mkdir("myproject")

os.chdir(Path.home() / "myproject")
run_process(['virtualenv myprojectenv'])
run_process(['. myprojectenv/bin/ativate'])

env_pkgs = []
for package in env_pkgs:
    if check_pkg(package):
        continue
    else:
        install_pkg(package)


src_file = "/home/achira/Desktop/achira/Desktop/configuration/backend/flask_copy.py"

if  not is_port_open(host, 5000):
    if not root():
        @set_root_and_run
        def allow_port():
            run_process(['sudo ufw allow 5000'])
