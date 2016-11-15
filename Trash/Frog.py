'''
Created on 14 ott 2016

@author: Conny
'''
'''
from Client import Frog
from Model import Model
import time
import json

x= Frog.Frog()
while True:

    x.device().filter(lambda d: d.location==Model.structure.location_type.livingroom or d.id=="2" or d.device==Model.structure.device_type.sensor_temp)
        .set(Model.structure.device.sensor_temp.temperature.name,15,lambda x : x).print()
    
    
    .set(Model.structure.device.sensor_temp.temperature.name,15,lambda x : x)

    x.device().filter(lambda d: d.location==Model.structure.location_type.livingroom or d.id=="2" or d.device==Model.structure.device_type.sensor_temp).print()
    print(x.device().filter(lambda d: d.device==Model.structure.device_type.sensor_temp).map(lambda x:x.temperature).reduce(lambda x,y: (x+y)/2))
    time.sleep(5)

    





from Client import Mqtt
from attrdict.dictionary import AttrDict
import json

class Frog(object):
    
    def __init__(self):
        self.middleware=Mqtt.Mqtt()
        self.data = []
        
    def filter(self,func):
        self.data = list(filter(func ,self.data))
        return self

    def device(self):
  
        self.data = self.middleware.getDevices()
 
        self.data=[]
        for i in self.middleware.getDevices():
            self.data.append(AttrDict(i))
        return self
        
    def map(self,func):
        self.data=list(map(func,self.data))
        return self
    
    def list(self):
        return list(self.data)

    
  
    
    def print(self):
        for i in self.data:
            print(json.dumps(i))
        return self
    
    def reduce(self,func):
        first=True
        value=0
        it = iter(self.data)
        for element in it:
            if first:
                value=element
                first=False
            else:
                value=func(value, element)
        return value
  '''  