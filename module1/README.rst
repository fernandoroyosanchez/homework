Bash script to initiate N instances of a docker image
===========================================================

This module includes a simple bash script to initiate N instances of a docker image.

It will produce an output based on:

<ID container> <netns_path_container>

Example 
user@ns3070194:~/homework/module1# sh start_containers.sh centos 3
3ed26c0ef61e /var/run/netns/3ed26c0ef61e
4ab76973deee /var/run/netns/4ab76973deee
153fd20ef61a /var/run/netns/153fd20ef61a

---------------

