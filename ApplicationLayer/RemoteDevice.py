'''
Created on 21 nov 2016

@author: Conny
'''
import json,time
from Dev.Device import Device
class RemoteDevice(object):
    '''
    classdocs
    '''
    ready=False
    def __init__(self ,device,read_only=True,shadow=None):
        '''
        Constructor
        '''
        self.device=device
        self.read_only=read_only
        self.ready=True
        self.shadow=shadow
        
    def __getattr__(self, name):
        return getattr(self.device,name)
    
    def __setattr__(self, name, value):
        if self.ready:
            if not(self.read_only):
                return setattr(self.device, name,value)
        else:
            return object.__setattr__(self, name, value)  
        
    def lock(self):
        if not(self.read_only) and self.shadow!=None:
                return self.shadow.lock(self.device.id)
        return False
                
    def unlock(self):
        if not(self.read_only) and self.shadow!=None:
            return self.shadow.unlock(self.device.id)
        return False   

d=Device("dev1","bath","device")
print("Device ready")
r=RemoteDevice(d,True)
print("Remote ready")
time.sleep(3)
print(r.location)
r.location=5
print(r.location)
print(d.location)
print(r.device)

print(r.lock())
