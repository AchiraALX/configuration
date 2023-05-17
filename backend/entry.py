#!/usr/bin/env python3
"""
    Entry point to configuration in the backend server
    The sole purpose of this file is to ensure that
    the environment is ready to run the configuration file
    conf.py

"""

from funcs import (
    check_pkg,
    install_pkg,
    check_apt_pkg,
    set_root_and_run,
)

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

# My name is Achira
# I am a software engineer
# I am a full stack engineer

# If you are using this file ensure that
# you have funcs.py and conf.py in the same directory