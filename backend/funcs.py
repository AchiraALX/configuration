#!/usr/bin/env python3
"""Separate functions from conf.py"""

import apt
from classes import Stack
from functools import wraps
import getpass
import os
from pathlib import Path
import pkg_resources
import shutil
import socket
import subprocess
import systemd

stack = Stack()

def check_pkg(pkg_name):
    try:
        pkg_resources.get_distribution(pkg_name)
        print(f"{pkg_name} resource was found.")
        return True

    except pkg_resources.DistributionNotFound:
        return False


def check_apt_pkg(pkg_name):
    apt_cache = apt.Cache()
    if pkg_name in apt_cache:
        package = apt_cache[pkg_name]
        if package.is_installed:
            print(f"{pkg_name} is installed.")
            return True
        else:
            return False

    else:
        return False


def install_pkg(pkg_name):
    if subprocess.check_call(['pip3', 'install', pkg_name]) == 0:
        print(pkg_name + "installed successfully")

    else:
        print("An error was encountered during the installation process")


def is_port_open(host, port):
    """Check if a port is open on a given host"""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        if result == 0:
            print(f"host={host!r}, port={port!r} is listening")
            return True


        else:
            return False

        sock.close()

    except socket.error:
        return False
        sock.close()


def copy_file(src, dst):
    """Copy a file from src to dst"""
    try:
        shutil.copy2(src, dst)
        print(f"Copied {src} to {dst} as successfully!")
        return 0

    except IOError as e:
        print("An error occurred during the process")
        return 1


def set_root_and_run(command_func):
    """Run a command with elevated privileges"""
    @wraps(command_func)
    def wrapper(*args, **kwargs):
        with subprocess.Popen(
            ["sudo", "-S"] + command_func(*args, **kwargs),
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT
        ) as process:
            # Pass the password to sudo through stdin
            process.communicate(input=f"{pass_handler()}\n".encode())

            # Capture and decode the output
            output = process.communicate()[0].decode()

        # Print the captured output
        print(output)

        return process.returncode

    return wrapper


def pass_handler() -> str:
    """Handle the password prompt"""
    # Check if the the password is in the stack
    if not stack.get("password"):
        stack.push("password", getpass.getpass("Enter your password: "))

    return str(stack.get("password"))


def test_nginx():
    """Test nginx configuration"""
    @set_root_and_run
    def test():
        return ["nginx", "-t"]

    return test()



# My name is Achira
# I am an ALX student
# I am pursuing software engineering

# Path: backend/funcs.py
