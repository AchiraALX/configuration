#!/bin/bash

# Define variables
server1="52.205.216.235"
server2="3.80.18.178"
share="/path/to/share"
mount_point="/mnt/shared"

# Install NFS client package (if needed)
apt-get install -y nfs-common

# Create mount point directory (if needed)
mkdir -p $mount_point

# Mount shared file system from server 1
mount -t nfs $server1:$share $mount_point

# Mount shared file system from server 2
mount -t nfs $server2:$share $mount_point

# Verify mount points
mount | grep $mount_point
