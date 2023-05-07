#!/usr/bin/env bash
# This script is used to run configuration files

# Install nginx
install_nginx() {
    echo "Installing nginx..."
    apt-get update
    apt-get install -y nginx-core
    echo "Starting nginx service..."
    systemctl start nginx
}

# Install mysql-server
install_mysql() {
    echo "Installing mysql-server..."
    apt-get update
    apt-get install -y mysql-server
    echo "Starting mysql service..."
    systemctl start mysql
}

for command in nginx mysql; do
    if ! command -v $command &> /dev/null; then
        install_$command
    fi
done

for command in nginx mysql; do
    if systemctl -q is-active $command.service; then
        echo "$command service is already running"
    else
        echo "Starting $command service..."
        systemctl start $command.service
    fi
done

# Echo the contents in the default file to /etc/nginx/sites-available/default
# This will overwrite the contents in the file
puppet apply ./backend/back.pp

# If host name is web01
# puppet apply web01.pp
# If host name is web02
# puppet apply web02.pp

if [[ $(hostname) == "web01" ]]; then
    puppet apply ./web01/web01.pp
elif [[ $(hostname) == "web02" ]]; then
    puppet apply ./web02/web02.pp
fi
