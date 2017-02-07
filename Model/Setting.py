'''
Created on 26 ott 2016

@author: Conny
'''
from pathlib import Path
import yaml

import subprocess

#Framework
path="./"

def getNodeId():
    path = Path("./Settings/").absolute()
    path=path.joinpath("NodeRegistry.yaml")
    nodes=yaml.load(open(str(path),'r'))
    with open("/etc/hostname") as f:
        host = f.readlines()
    
    ip=subprocess.Popen("hostname -i", stdout=subprocess.PIPE, stderr=None, shell=True)
    output = ip.communicate()
    
    for node in nodes['node_templates']:  
        return node+":"+host+":"+output[0]


def getBrokerIp():
    path = Path("./Settings/").absolute()
    path=path.joinpath("NodeRegistry.yaml")
    nodes=yaml.load(open(str(path),'r'))
    for node in nodes['node_templates']:  
        return nodes['node_templates'][node]['attributes']['broker_address']
    
