#!/usr/bin/env bash
# Running this script will ensure that all dependencies
# are available and their services are running

# Define functions for missing dependencies
install_curl() {
    echo "Installing curl..."
    apt-get update
    apt-get install -y curl
}

install_puppet() {
    echo "Installing puppet..."
    apt-get update
    apt-get install -y puppet
}

# Check if the user is root
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root"
   exit 1
fi

# Check if the user has sudo privileges
if ! sudo -v; then
    echo "This script must be run with sudo privileges"
    exit 1
fi

# Check if the user has the required dependencies
for command in curl puppet; do
    if ! command -v $command &> /dev/null; then
        echo "Command $command is missing"
        # Call the appropriate function to install the missing dependency
        install_${command}
    fi
done

# Decrypt the configuration files
openssl enc -aes-256-cbc -iter 10000 -d -in ./load_balancer/config.cfg.enc -out ./load_balancer/config.cfg
openssl enc -aes-256-cbc -iter 10000 -d -in ./backend/default.enc -out ./backend/default

# Check if the server is a load balancer
hostname="$(uname -n)"
if [[ "$hostname" == *lb* ]]; then
    ./load_balancer/main.sh
fi

# Check if the server is a web server
if [[ "$hostname" == *web* ]]; then
    ./backend/main.sh
fi
