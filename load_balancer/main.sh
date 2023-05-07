#!/usr/bin/env bash

# Install certbot
install_certbot() {
    echo "Installing certbot..."
    apt-get update
    apt-get install -y certbot
}

# Install mysql-client
install_mysql() {
    echo "Installing mysql-client..."
    apt-get update
    apt-get install -y mysql-client-core-8.0
}

# Install haproxy
install_haproxy() {
    echo "Installing haproxy..."
    apt-get update
    apt-get install -y haproxy
    echo "Starting haproxy service..."
    systemctl start haproxy
}

for command in haproxy certbot mysql; do
    if ! command -v $command &> /dev/null; then
        install_$command
    fi
done

for command in haproxy; do
    if systemctl -q is-active $command.service; then
        echo "$command service is already running"
    else
        echo "Starting $command service..."
        systemctl start $command.service
    fi
done

cat *.cfg > /etc/haproxy/haproxy.cfg
