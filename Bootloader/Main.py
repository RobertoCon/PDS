'''
Created on 06 gen 2017

@author: Conny
'''
from Model.ApplicationManager import ApplicationManager
from Model.DeviceManager import DeviceManager
from Model.NodeManager import NodeManager
from Model.LoadManager import LoadManager
import time

if __name__ == '__main__':
    n=NodeManager()
    d=DeviceManager()
    a=ApplicationManager()
    l=LoadManager()
    
    
    while True:
        time.sleep(1)