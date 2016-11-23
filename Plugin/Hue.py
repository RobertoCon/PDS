'''
Created on 08 nov 2016

@author: Conny
'''

from Dev.Device import Device
from Dev.ActiveDevice import ActiveDevice
import json
import time

class Hue(Device):

    def __init__(self,id_dev="",location_dev="unknown",light=False):
        super(Hue, self).__init__(id_dev, location_dev, type_dev="Hue")
        self.light=light
         
    #redefine how to serialize the struct
    def to_json(self):
        struct = {}
        struct['id'] = self.id
        struct['location'] = self.location
        struct['type'] = self.type
        struct['light'] = self.light
        return json.dumps(struct)
        
    def from_json(self,serial_dict):
        struct=json.loads(str(serial_dict))
        self.id = struct['id']
        self.location =struct['location'] 
        self.type=struct['type']
        self.light=struct['light']
        return self
        
    @staticmethod          
    def make_active(device):
        #Define Handlers here
        def light(message , active):
            #print("WriteRequest : ",message.payload.decode("utf-8"))
            active.dev.light=message['value'] in ["True","true","y"]
            active.publish()
                
        handlers=[("/device/"+device.id+"/light",light)] #[("topic1",function1),("topic2",function2)] like [("/device/"+id_dev+"/light",function)]
        #Define Job to perform periodically
        def job_to_do(active):
            while True:
                active.publish()
                time.sleep(10)            
        return ActiveDevice(device,job_to_do,handlers)
    