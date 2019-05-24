# -*- coding: utf-8 -*-
import sys
import os

""" Set of functions to facilitate some commons tasks  as work with paths
ask to the user info by stdin, etc.

"""

def get_netns_paths():
    """Obtains netns path from stdin 
        if argv -pathsinline is passed, user will be ask
        to be introduced manually a list of comma separate paths

    Args:
        empty

    Returns:
        attr1, attr2 (array, array): tuple attr1 array of netns_paths, attr2 is 
        the last part of the url passed in the netns_path

    """
    paths = []
    if len(sys.argv) > 1:
        if '-pathsinline' in sys.argv: 
            print('Please provide net_ns_path separated by comma')
            paths=sys.stdin.readline()
            paths=paths.split(',')
    else:
        for line in sys.stdin:
            paths.append(line)

    paths = [x.strip(' ').rstrip('\n') for x in paths]
    paths = [x for x in paths if x]
    paths_id = [get_id_netnspath(x) for x in paths]
    return paths, paths_id

def get_id_netnspath(path):
    """Obtains last part of the netns os path. Normally as /var/run/netns/XXXXX
    
    Args:
        path (string): path url

    Returns:
        path (string): last part of the path 

    """
    return os.path.basename(os.path.normpath(path))

def initiate_containers(_docker_image, _instances):
    """Start of containers using system call to bash script developed in module1 folder and return a list of tuples (id, path_to_ns_net)
    
    Args:
        _docker_image (string): name of the docker image to start
        _instances (integer): number of instances to start 

    Return:
        The output of this function if a list of tuples in format "CONTAINER_ID NETNS_PATH_OF_THE_CONTAINER"
        
    """
    session = subprocess.Popen(['../module1/start_containers.sh', _docker_image, _instances], stdout=PIPE, stderr=PIPE)
    stdout, stderr = session.communicate()

    if stderr:
        raise Exception("Error initializing containers: "+str(stderr))
