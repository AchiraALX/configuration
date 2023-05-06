#!/usr/bin/env bash
# Running this script will ensure that all dependencies
# are available and their services are running

# Define functions for missing dependencies
install_curl() {
    echo "Installing curl..."
    apt-get update
    apt-get install -y curl
}

install_nginx() {
    echo "Installing nginx..."
    apt-get update
    apt-get install -y nginx
    echo "Starting nginx service..."
    systemctl start nginx
}

install_certbot() {
    echo "Installing certbot..."
    apt-get update
    apt-get install -y certbot
}

install_puppet() {
    echo "Installing puppet..."
    apt-get update
    apt-get install -y puppet
}

install_mysql() {
    echo "Installing mysql..."
    apt-get update
    apt-get install -y mysql
    echo "Starting mysql service..."
    systemctl start mysql
}

install_haproxy() {
    echo "Installing haproxy..."
    apt-get update
    apt-get install -y haproxy
    echo "Starting haproxy service..."
    systemctl start haproxy
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
for command in curl nginx certbot puppet mysql haproxy; do
    if ! command -v $command &> /dev/null; then
        echo "Command $command is missing"
        # Call the appropriate function to install the missing dependency
        install_${command}
    fi

    # Check if the dependency has a service
    if systemctl -q is-active $command.service; then
        echo "$command service is already running"
    else
        echo "Starting $command service..."
        systemctl start $command.service
    fi
done
