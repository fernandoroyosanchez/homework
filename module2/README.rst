Docker netlink over bridge using pyroute2 Module Repository
===========================================================

This project includes a small piece of software mainly motivated to configure a subnet of docker containers (through its namespaces net ns) 
over a bridge interface allocate in the host.

Main program to configure a subnet over several namespaces netns all of them connected to a linux bridge interface. Mainly motivated by the 
idea to communicate among them several docker containers deployed over a host.

To execute, here are some examples, according to the arguments provided

1) Execution passing netns path over stdin manually by a user

user@ns3070194:~/module2# python net_containers.py -pathsinline
Please provide net_ns_path separated by comma
/var/run/netns/ff33a026102a,/var/run/netns/49784f4c9432,/var/run/netns/0ec96b572002
ff33a026102a 10.0.0.1/24
49784f4c9432 10.0.0.2/24
0ec96b572002 10.0.0.3/24

2) Execution passing netns path automatically from pipe stdin (e.g. using bash script on module1/start_containers.sh)
user@ns3070194:~/module1# sh start_containers.sh kuryr/demo 3 > ../module2/path.log
user@ns3070194:~/module2# cat path.log 
185bbbf447b7 /var/run/netns/185bbbf447b7
8ee28bb14099 /var/run/netns/8ee28bb14099
5b993c4bc201 /var/run/netns/5b993c4bc201
user@ns3070194:~/module2# cat path.log | awk '{print $2}' | python net_containers.py
185bbbf447b7 10.0.0.1/24
8ee28bb14099 10.0.0.2/24
5b993c4bc201 10.0.0.3/24

The output of a correct execution should be the list of IDs of the namespaces netns and IP address and netmask asigned

After that you can curling to test the communication among docker containers

user@ns3070194:~/module2# ip netns exec 185bbbf447b7 curl -X GET http://10.0.0.1:8080
185bbbf447b7: HELLO! I AM ALIVE!!!
user@ns3070194:~/module2# ip netns exec 185bbbf447b7 curl -X GET http://10.0.0.2:8080
8ee28bb14099: HELLO! I AM ALIVE!!!
user@ns3070194:~/module2# ip netns exec 185bbbf447b7 curl -X GET http://10.0.0.3:8080
5b993c4bc201: HELLO! I AM ALIVE!!!
user@ns3070194:~/module2# ip netns exec 8ee28bb14099 curl -X GET http://10.0.0.3:8080
5b993c4bc201: HELLO! I AM ALIVE!!!
user@ns3070194:~/module2# ip netns exec 8ee28bb14099 curl -X GET http://10.0.0.2:8080
8ee28bb14099: HELLO! I AM ALIVE!!!
user@ns3070194:~/module2# ip netns exec 8ee28bb14099 curl -X GET http://10.0.0.1:8080
185bbbf447b7: HELLO! I AM ALIVE!!!
user@ns3070194:~/module2# ip netns exec 5b993c4bc201 curl -X GET http://10.0.0.1:8080
185bbbf447b7: HELLO! I AM ALIVE!!!
user@ns3070194:~/module2# ip netns exec 5b993c4bc201 curl -X GET http://10.0.0.2:8080
8ee28bb14099: HELLO! I AM ALIVE!!!
user@ns3070194:~/module2# ip netns exec 5b993c4bc201 curl -X GET http://10.0.0.3:8080
5b993c4bc201: HELLO! I AM ALIVE!!!

---------------

