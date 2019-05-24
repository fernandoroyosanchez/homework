# -*- coding: utf-8 -*-

from pyroute2 import IPDB, NetNS
import helpers
import logging
import traceback

"""Class controller for the use of iproute2.IPDB netlink module

        It includes methods to interact with a IPDB object, local or remote (netns), and 
        do traditional operations over it as add/modify interfaces 

"""

class Ipdb:

    def __init__(self):
        self.ipdb_controller = None

    def connect(self, netnspath=None):
        """Initializa a IPDB object local or over remote netns
        
        Args:
            param1 (string): The netns path to connect for remote management
        """

        try:
            if netnspath:
                self.ipdb_controller = IPDB(nl=NetNS(netnspath))
            else:
                self.ipdb_controller = IPDB()
        except Exception:
            logging.error('Cannot connect to the namespace indicate')
            return

    def create_interface_bridge(self, name):
        """Create a linux bridge interface over ipdb, 

        Args:
           name (string): iface name to create
                        
        """
        try:
            if self.ipdb_controller:
                self.ipdb_controller.create(ifname=name, kind='bridge').commit()
        except Exception:
            logging.error('Cannot create linux bridge interface')
            return

    def create_interface(self, name, peer_id=None):
        """Create interface veth over ipdb, returning a tuple of the iface names created

        Args:
           name (string): iface name to create
           peer_id (string)(optional): According to the type, it is used to compose the iface name of the peer associated

        Returns:
           attr1, attr2 (string, string): tuple of interface names created
            
        """
        try:
            if self.ipdb_controller:
                name_iface_peer = name+'_'+peer_id
                self.ipdb_controller.create(ifname=name, kind='veth', peer=name_iface_peer).commit()
                return name, name_iface_peer
        except Exception:
            logging.error('Cannot create interface')
            return  '',''      
            

    def change_status_interface(self, name, status):
        """Change the status of interface to up|down

        Args:
           name (string): iface name to create
           status (string): status change to (up|down)
            
        """

        try:
            with self.ipdb_controller.interfaces[name] as iface:
                if status == 'up':
                    iface.up()
                if status == 'down':
                    iface.down()
        except Exception:
            logging.error('Cannot change interface status')
            return

    def move_interface_tonetns(self, name, netns):
        """Move inteface to another namespace

        Args:
           name (string): iface name to create
           status (string): status change to (up|down)
            
        """

        try:
            with self.ipdb_controller.interfaces[name] as iface:
                iface.net_ns_fd = netns
        except Exception:
            logging.error('Cannot change interface to ' + netns
                          + ' namespace')
            return

    def add_port_interface(self, name, iface_port):
        """Add port to interface (normally for bridge ones)
        
        Args:
           name (string): iface name to attach port
           iface_port (string): iface name to be attached
            
        """

        try:
            with self.ipdb_controller.interfaces[name] as iface:
                iface.add_port(iface_port)
        except Exception:
            logging.error('Cannot add port to interface')
            return

    def change_addr_interface(self, name, ip, mask):
        """Change addr to interface
        
        Args:
           name (string): iface name modify ip_addr
           ip (string): ip address to establish
           mask (string): netmask to establish
           
        """

        try:
            with self.ipdb_controller.interfaces[name] as iface:
                iface.add_ip(ip+'/'+mask)
        except Exception:
            logging.error('Cannot add port to interface')
            return



			
			