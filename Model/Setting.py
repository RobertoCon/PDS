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
    for node in nodes['node_templates']:  
        return nodes['node_templates'][node]['id']


def getBrokerIp():
    path = Path("./Settings/").absolute()
    path=path.joinpath("NodeRegistry.yaml")
    nodes=yaml.load(open(str(path),'r'))
    for node in nodes['node_templates']:  
        return nodes['node_templates'][node]['attributes']['broker_address']
    
def getHostName():
    return subprocess.getoutput("hostname")

def getIp():
    return subprocess.getoutput("hostname -i")
    
