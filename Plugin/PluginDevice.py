'''
Created on 17 nov 2016

@author: Conny
'''

from Dev.Device import Device
from Dev.ActiveDevice import ActiveDevice
import json
import time

class PluginDevice(Device):

        def __init__(self,id_dev="",location_dev="unknown"):   #plus other attribute
            
            super(PluginDevice, self).__init__(id_dev, location_dev, type_dev="PluginDevice")
            #Set not base attribute
         
         
        #redefine how to serialize the struct
        def to_json(self):
            struct = {}
            struct['id'] = self.id
            struct['location'] = self.location
            struct['type'] = self.type
            return json.dumps(struct)
        
        
        def from_json(self,serial_dict):
            struct=json.loads(str(serial_dict))
            self.id = struct['id']
            self.location =struct['location'] 
            self.type=struct['type']
            return self
    
              
        @staticmethod          
        def make_active(device):
            #Define Handlers here
                
            handlers=[] #[("topic1",function1),("topic2",function2)] like [("/device/"+id_dev+"/light",function)]
            #Define Job to perform periodically
            def job_to_do(active):
                while True:
                    active.publish()
                    time.sleep(10)
            print("Ready : ",device)        
            return ActiveDevice(device,job_to_do,handlers)
        
    