#!/usr/bin/env python3
""" Initialize the backend """

from funcs import *

if __name__ == "__main__":
    welcome_user(user())
    print("Initializing the backend...\n")

    run_process(['./entry.py'])
