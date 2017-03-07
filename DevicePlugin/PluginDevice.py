'''
Created on 17 nov 2016

@author: Conny
'''

from Device.Device import Device
from Device.ActiveDevice import ActiveDevice
import json
import time

class PluginDevice(Device):

        def __init__(self,id_dev="",location_dev="unknown"):   #plus other attribute
            
            super(PluginDevice, self).__init__(id_dev, location_dev, type_dev="PluginDevice")
            #Set not base attribute
         
        def to_text(self):
            struct = {}
            struct['id_dev'] = self.id
            struct['location_dev'] = self.location
            struct['type_dev'] = self.type
            return json.dumps(struct)
        
        def from_text(self,serial_dict):
            struct=json.loads(str(serial_dict))
            self.id = struct['id_dev']
            self.location =struct['location_dev'] 
            self.type=struct['type_dev']
            return self
    
              
        @staticmethod          
        def make_active(device,broker_ip=""):
            #Define Handlers here
                
            handlers=[] #[("topic1",function1),("topic2",function2)] like [("/device/"+id_dev+"/light",function)]
            #Define Job to perform periodically
            def job_to_do(active):
                while True:
                    active.publish()
                    time.sleep(10)      
            return ActiveDevice(device,job_to_do,handlers)
        
    