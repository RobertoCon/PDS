'''
Created on 08 nov 2016

@author: Conny
'''

from Device.Device import Device
#from Device.ActiveDevice import ActiveDevice
from Device.ActiveDevicePoolThread  import ActiveDevice
import json
import time
import random

class Pir(Device):

    def __init__(self,id_dev="",location_dev="unknown",state=False):
        super(Pir, self).__init__(id_dev, location_dev, type_dev="Pir")
        self.state=state
        self.timestamp=time.time()
         
    def to_text(self):
        array=[]
        array.append(self.id)
        array.append(self.location)
        array.append(self.type)
        array.append(self.time_resolution)
        array.append(self.timestamp)
        array.append(self.state)
        return json.dumps(array)   
        
        
    def from_text(self,serial_dict):
        struct=json.loads(str(serial_dict))
        if type(struct)  is list:
            self.id=struct[0]
            self.location=struct[1]
            self.type =struct[2]
            self.time_resolution=struct[3]
            self.timestamp=struct[4]
            self.state =struct[5]
        else:
            self.id = struct['id_dev']
            self.location =struct['location_dev'] 
            self.type=struct['type_dev']
            self.time_resolution=struct['time_resolution']
            self.timestamp=struct['timestamp']
            self.state=struct['state']
        return self    
        
    @staticmethod          
    def make_active(device):
        #Define Handlers here    
        handlers=[] #[("topic1",function1),("topic2",function2)] like [("/device/"+id_dev+"/light",function)]
        #Define Job to perform periodically
        def job_to_do(active):
                with active.locker: 
                    active.dev.state=random.choice([True,False])
                    active.dev.timestamp=time.time()
                    active.publish()            
        return ActiveDevice(device,job_to_do,handlers)
    