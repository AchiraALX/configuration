#!/usr/bin/env python3
"""Some configuration on web01"""
from funcs import *
import getpass
import os
from pathlib import Path
import socket
import subprocess
import sys

packages = ['virtualenv', 'numpy', 'flask', 'gunicorn']

for i in packages:
    if check_pkg(i):
        continue
    else:
        install_pkg(i)

os.chdir(Path.home())
dirs = os.listdir(Path.home())

if "myproject" not in dirs:
    os.mkdir("myproject")

os.chdir(Path.home() / "myproject")
# Check if the environment already exists
if not os.path.isdir("myprojectenv"):
    run_process(['virtualenv myprojectenv'])

os.chdir(Path.home() / "myproject")

# Install packages in the environment
env_pkgs = ['gunicorn', 'flask']
for package in env_pkgs:
    if check_pkg(package):
        continue
    else:
        install_pkg(package)

apt_packages = ['gunicorn']
for package in apt_packages:
    if check_apt_pkg(package):
        continue
    else:
        @set_root_and_run
        def install_apt_pkg():
            print(f"Authenticate to install {package}")
            print(f"Installing {package}...")
            return ["apt-get", "install", package]
        install_apt_pkg()


src_flask = "/home/achira/Desktop/achira/Desktop/configuration/backend/flask_copy.py"
dest_flask = f"/home/{user()}/myproject/myproject.py"
src_wsgi = "/home/achira/Desktop/achira/Desktop/configuration/backend/wsgi_copy.py"
dest_wsgi = f"/home/{user()}/myproject/wsgi.py"

if  not is_port_open(host(), 5000):
    if not root():
        @set_root_and_run
        def allow_port():
            return ["ufw", "allow", "5000"]
        allow_port()
        print("Allowing port 5000...")


copy_file(src_flask, dest_flask)
copy_file(src_wsgi, dest_wsgi)


if user() == "achira":
    @set_root_and_run
    def copy_service():
        return ["cp /home/achira/Desktop/achira/Desktop/configuration/backend/myproject_achira.service /etc/systemd/system/"]

    copy_service()
    print("Copying achira service...")

else:
    @set_root_and_run
    def copy_service():
        return ["cp /home/{user()}/configuration/myproject.service /etc/systemd/system/"]

    copy_service()
    print("Copying service...")


service = ["myproject_achira" if user() == "achira" else "myproject"]
for service in service:
    try:
        @set_root_and_run
        def daemon_reload():
            return ["systemctl", "daemon-reload"]

        daemon_reload()
        print("Reloading daemon...")

        if check_service(service) == 0:
            @set_root_and_run
            def start_service():
                return ["systemctl", "start", service]

            start_service()
            print(f"Starting {service}...")

            @set_root_and_run
            def enable_service():
                return ["systemctl", "enable", service]

            enable_service()
            print(f"Enabling {service}...")
        else:
            @set_root_and_run
            def restart_service():
                return ["systemctl", "restart", service]

        run_process(['service myproject_achira status'])

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while starting {service}")
        print(e)

default_nginx = [
    "/etc/nginx/sites-enabled/default",
    "/etc/nginx/sites-available/default"
]

for i in default_nginx:
    if os.path.isfile(i):
        @set_root_and_run
        def delete_default():
            return ["rm", i]

        delete_default()
        print("Deleting default nginx...\n")

src_local_nginx = "/home/achira/Desktop/achira/Desktop/configuration/backend/nginx_copy"
dest_local_nginx = "/etc/nginx/sites-available/default"

@set_root_and_run
def copy_nginx():
    return ["cp", src_local_nginx, dest_local_nginx]

copy_nginx()
print("Copying nginx...\n")

myproject_link = os.path.islink("/etc/nginx/sites-enabled/default")

if myproject_link:
    @set_root_and_run
    def enable_nginx():
        return ["ln", "-s", dest_local_nginx, "/etc/nginx/sites-enabled"]

    print("Enabling nginx...\n")
    enable_nginx()

else:
    print("Nginx already enabled\n")

if test_nginx() == 0:
    print("Nginx configuration test passed\n")
    @set_root_and_run
    def restart_nginx():
        return ["systemctl", "restart", "nginx"]

    restart_nginx()
    print("Restarting nginx...\n")

    run_process(['service nginx status'])

else:
    print("Nginx configuration test failed\n")

print()

@set_root_and_run
def delete_5000():
    return ["ufw", "delete", "5000"]

delete_5000()
print("Deleting port 5000...\n")

@set_root_and_run
def allow_nginx():
    return ["ufw", "allow", "Nginx Full"]

allow_nginx()
print("Allowing Nginx Full...\n")

print("Deployment complete\n")

# run gunicorn --bind
# run_process(['gunicorn', '--bind', '0:5000', 'wsgi:app'])



# My name is Achira
# I am an ALX student
# I am a software engineer

# If you are using this file make sure als the funcs.py
# file is in the same directory as this file
