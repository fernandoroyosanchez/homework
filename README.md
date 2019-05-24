# homework


# Project Title

This project includes two modules.

### Module 1 - Bash script to initiate N instances of a docker image

Bash script to initiate N instances of a docker image

This module includes a simple bash script to initiate N instances of a docker image.

### Module 2 - Namespaces netlink over bridge using pyroute2 Module Repository

This project includes a small piece of software mainly motivated to configure a subnet of docker containers(through its namespaces net ns)  or any other namespace over a bridge interface allocate in the host.

Main program to configure a subnet over several namespaces netns all of them connected to a linux bridge interface. Mainly motivated by the idea to communicate among them several docker containers deployed over a host.

### Prerequisites

This software should be required:

* Docker installed
* Python 2.7 or higher
* Library pyroute2 


### Running

To run module1 here you have an example

```
user@ns3070194:~/homework/module1# sh start_containers.sh centos 3
3ed26c0ef61e /var/run/netns/3ed26c0ef61e
4ab76973deee /var/run/netns/4ab76973deee
153fd20ef61a /var/run/netns/153fd20ef61a
```

To run module2 you have several options.

* 1) Execution passing netns path over stdin manually by a user

```
user@ns3070194:~/module2# python net_containers.py -pathsinline
Please provide net_ns_path separated by comma
/var/run/netns/ff33a026102a,/var/run/netns/49784f4c9432,/var/run/netns/0ec96b572002
ff33a026102a 10.0.0.1/24
49784f4c9432 10.0.0.2/24
0ec96b572002 10.0.0.3/24
```

* 2) Execution passing netns path automatically from pipe stdin (e.g. using bash script on module1/start_containers.sh)

```
user@ns3070194:~/module1# sh start_containers.sh kuryr/demo 3 > ../module2/path.log
user@ns3070194:~/module2# cat path.log 
185bbbf447b7 /var/run/netns/185bbbf447b7
8ee28bb14099 /var/run/netns/8ee28bb14099
5b993c4bc201 /var/run/netns/5b993c4bc201
user@ns3070194:~/module2# cat path.log | awk '{print $2}' | python net_containers.py
185bbbf447b7 10.0.0.1/24
8ee28bb14099 10.0.0.2/24
5b993c4bc201 10.0.0.3/24
```

The output of a correct execution should be the list of IDs of the namespaces netns and IP address and netmask asigned

After that you can curling to test the communication among docker containers

```
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
```



## Authors

* **Fernando Royo** - *Initial work* - [Git](https://github.com/fernandoroyosanchez)



