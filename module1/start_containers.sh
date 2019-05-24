#!/usr/bin/env bash
set -e

# Check params
if [  $# -ne 2 ] 
then  
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

