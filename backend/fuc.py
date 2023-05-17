#!/usr/bin/env python3

import subprocess
import getpass
from functools import wraps

def run_with_elevation(command_func):
    @wraps(command_func)
    def wrapper(*args, **kwargs):
        # Get the current user
        current_user = getpass.getuser()

        # Run the command with elevated privileges
        with subprocess.Popen(["sudo", "-S"] + command_func(*args, **kwargs), stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as process:
            # Pass the password to sudo through stdin
            process.communicate(input=f"{getpass.getpass()}\n".encode())

            # Capture and decode the output
            output = process.communicate()[0].decode()

        # Print the captured output
        print(output)

        return process.returncode

    return wrapper

# Example usage
@run_with_elevation
def run_command_with_elevation():
    # Command to run with elevated privileges
    command_with_elevation = ["apt-get", "update"]
    return command_with_elevation

run_command_with_elevation()
