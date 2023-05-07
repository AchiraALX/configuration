#!/usr/bin/env bash
# This script is used to run configuration files

# Echo the contents in the default file to /etc/nginx/sites-available/default
# This will overwrite the contents in the file
cat default > /etc/nginx/sites-available/default

# If host name is web01
# puppet apply web01.pp
# If host name is web02
# puppet apply web02.pp

if [[ $(hostname) == "web01" ]]; then
    puppet apply ./web01/web01.pp
elif [[ $(hostname) == "web02" ]]; then
    puppet apply ../web02/web02.pp
fi
