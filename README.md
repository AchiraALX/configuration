# This directory will contain the configuration files
# for the servers (lib01, web01, and web02)

All the servers should have the following services
running:

    - Nginx
    - haproxy
    - certbot
    - MySQL
    - puppet-agent
    - curl

Puppet will be checked first and if not installed
it will be installed
