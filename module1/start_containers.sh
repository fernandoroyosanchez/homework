#!/usr/bin/env bash
set -e

#### Functions ###
display_usage() { 
	echo "This script must be run with root privileges and"
	echo "docker should be installed!" 
	echo "\nUsage:\n$0 <docker_image> <instances>\n" 
	echo " <saved_image>\t\tThe image file to run" 	
	echo " <instances>\t\tnumber of instances to start" 	
	echo "\nExample: $0 centos 3 "
} 

# Check params
if [  $# -ne 2 ] 
then  
	display_usage
	exit 1
fi 

# Check docker is executable
# 
docker images > /dev/null 2>&1; rc=$?;
if [ $rc != 0 ]; then 
	display_usage
	exit 1
fi

# Getting image from docker registry
echo "Getting $1 from docker registry"
docker pull $1 > /dev/null

# Generate simbolic link to namespace for containers
mkdir -p /var/run/netns

# Iterate over number of instances 
echo "Starting containers"
for i in `seq 1 $2` ; do
	__id=`docker run --detach $1 | cut -c1-12`
	__pid="$(docker inspect --format '{{.State.Pid}}' ${__id})"
	__path_ns_net="/var/run/netns/$__id"
	ln -sf /proc/$__pid/ns/net $__path_ns_net
	echo $__id $__path_ns_net
done


