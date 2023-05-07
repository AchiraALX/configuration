#!/bin/bash

# Get the hostname of the computer
hostname="$(uname -n)"

# Check if the hostname ends with "lb-01"
if [[ "$hostname" == *lb-01 ]]; then
  # Generate SSL certificate using Certbot
  certbot certonly --standalone -d blissprism -d "$hostname" -n --agree-tos --email achitrajacobs@gmail.com --preferred-challenges http-01 --http-01-port 8080

  # Print success message to the console
  echo "SSL certificate generated for hostname $hostname, IP address
