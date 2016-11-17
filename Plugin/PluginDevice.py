'''
Created on 17 nov 2016

@author: Conny
'''

from Dev.Device import Device
from Dev.ActiveDevice import ActiveDevice
import json
import time

class PluginDevice(Device):

        def __init__(self,id_dev="",location_dev=""):   #plus other attribute
            
            super(PluginDevice, self).__init__(id_dev, location_dev, type_dev="PluginDevice",lock_id="")
            #Set not base attribute
         
         
        #redefine how to serialize the struct
        def to_json(self):
            struct = {}
            struct['id'] = self.id
            struct['location'] = self.location
            struct['type'] = self.type
            struct['lock_id'] = self.lock_id
            return json.dumps(struct)
        
        
        def from_json(self,serial_dict):
            struct=json.loads(str(serial_dict))
            self.id = struct['id']
            self.location =struct['location'] 
            self.type=struct['type']
            self.lock_id= struct['lock_id']
            return self
    
              
        @staticmethod          
        def new_active_PluginDevice(id_dev ,location_dev,type_dev="PluginDevice",lock_id=""):
            def jobToDo(act):
                    while True:
                        act.publish()
                        time.sleep(10)
            return ActiveDevice(PluginDevice(id_dev ,location_dev,type_dev,lock_id),jobToDo,[])
        
        
    