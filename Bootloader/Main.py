'''
Created on 06 gen 2017

@author: Conny
'''
from Model.ApplicationManager import ApplicationManager
from Model.DeviceManager import DeviceManager
import time

if __name__ == '__main__':
    l=DeviceManager()
    a=ApplicationManager()
    
    while True:
        time.sleep(1)