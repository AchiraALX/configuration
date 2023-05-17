#!/usr/bin/env python3
"""Some configuration on web01"""
from funcs import *
import getpass
import os
from pathlib import Path
import socket
import subprocess


# Get the host name of the local machine
host = lambda: socket.gethostname()

# Get the username of the current user
user = lambda: getpass.getuser()

# Run a process
run_process = lambda args: subprocess.check_call(args, shell=True)

# Check if the current user is root
root = lambda: os.geteuid() == 0

packages = ['virtualenv', 'numpy', 'flask', 'gunicorn', "systemd"]

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
# Check if the environment already exists
if not os.path.isdir("myprojectenv"):
    run_process(['virtualenv myprojectenv'])

# Activate the environment
run_process(['. myprojectenv/bin/activate'])

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
        return ["cp", "/home/achira/Desktop/achira/Desktop/configuration/backend/myproject_achira.service", "/etc/systemd/system/"]

    copy_service()
    print("Copying service...")

else:
    @set_root_and_run
    def copy_service():
        return ["cp", f"/home/{user()}/configuration/myproject.service", "/etc/systemd/system/"]

    copy_service()
    print("Copying service...")


service = ["myproject" if user() == "achira" else "myproject_achira"]
for service in service:
    try:
        @set_root_and_run
        def daemon_reload():
            return ["systemctl", "daemon-reload"]

        daemon_reload()
        print("Reloading daemon...")

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

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while starting {service}")
        print(e)

src_local_nginx = "/home/achira/Desktop/achira/Desktop/configuration/backend/nginx_copy"
dest_local_nginx = "/etc/nginx/sites-available/myproject"

@set_root_and_run
def copy_nginx():
    return ["cp", src_local_nginx, dest_local_nginx]

copy_nginx()
print("Copying nginx...\n")

myproject_link = "/etc/nginx/sites-enabled/myproject"

if not myproject_link:
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

else:
    print("Nginx configuration test failed\n")

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



# My name is Achira
# I am an ALX student
# I am a software engineer

# If you are using this file make sure als the funcs.py
# file is in the same directory as this file
