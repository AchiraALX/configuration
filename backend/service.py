#!/usr/bin/env python3
"""Working with the service"""

from funcs import *
import os

file = "/home/achira/Desktop/achira/Desktop/configuration/backend/myproject_achira.service"
dest_file = "/etc/systemd/system/myproject_achira.service"

if os.path.exists(dest_file):
    print("File exists")
    run_process([f"ls -l {dest_file}"])
else:
    print("File not exists")
