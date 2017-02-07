'''
Created on 26 ott 2016

@author: Conny
'''
from pathlib import Path
import yaml

from subprocess import PIPE, run

#Framework
path="./"

def getNodeId():
    path = Path("./Settings/").absolute()
    path=path.joinpath("NodeRegistry.yaml")
    nodes=yaml.load(open(str(path),'r'))
    with open("/etc/hostname") as f:
        host = f.readlines()
    ip=run("hostname -i", stdout=PIPE, stderr=PIPE, universal_newlines=True)
    for node in nodes['node_templates']:  
        return node+":"+host+":"+ip.stdout

    

def getBrokerIp():
    path = Path("./Settings/").absolute()
    path=path.joinpath("NodeRegistry.yaml")
    nodes=yaml.load(open(str(path),'r'))
    for node in nodes['node_templates']:  
        return nodes['node_templates'][node]['attributes']['broker_address']
    
