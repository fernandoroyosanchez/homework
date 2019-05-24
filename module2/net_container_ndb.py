# -*- coding: utf-8 -*-
""" 
Main program to configure a subnet over several namespaces netns all of them connected to a linux bridge interface. Mainly motivated by the 
idea to communicate among them several docker containers deployed over a host.

To execute, this are some examples, according to the arguments provided

1) Execution passing netns path over stdin manually by a user

user@ns3070194:~/module2# python net_containers.py -pathsinline
Please provide net_ns_path separated by comma
/var/run/netns/ff33a026102a,/var/run/netns/49784f4c9432,/var/run/netns/0ec96b572002
ff33a026102a 10.0.0.1/24
49784f4c9432 10.0.0.2/24
0ec96b572002 10.0.0.3/24

1) Execution passing netns path automatically from pipe stdin (e.g. using bash script on module1/start_containers.sh)
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

"""

from core import helpers, ndb

# Create a linux brigde, with e.g 'homework' as name
bridge_name='homework'
ndb_h = ndb.Ndb()
ndb_h.connect()
ndb_h.create_interface_bridge(bridge_name)

# Get the list of paths to network namespace from stdin
netnspaths, netnspaths_ids = helpers.get_netns_paths()

# Configures a subnet for the aforementioned container in the 'homework' bridge so
# that each container has a unique address in the 'homework' subnet.
# The bridge should not have any address

net = "10.0.0."
ips_last_digit =  [ str(i) for i in range (1, len(netnspaths) + 1)]
mask = '24'

for (ip_last_digit, netnspath) in zip(ips_last_digit[0:len(netnspaths)], netnspaths_ids):
    ndb_ns = ndb.Ndb()
    ndb_ns.connect(netnspath)
    veth, veth_peer = ndb_h.create_interface('veth0', ip_last_digit)
    ndb_h.move_interface_tonetns(veth, netnspath)
    ndb_h.add_port_interface(bridge_name,veth_peer)
    ndb_h.change_status_interface(veth_peer, 'up')
    ndb_ns.change_status_interface(veth, 'up')
    ndb_ns.change_addr_interface(veth, net+ip_last_digit, mask)
    print(netnspath+' '+net+ip_last_digit+'/'+mask)

			