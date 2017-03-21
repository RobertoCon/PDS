'''
Created on 08 nov 2016

@author: Conny
'''

from Device.Device import Device
from Device.ActiveDevice import ActiveDevice
import json
import time

class Hue(Device):

    def __init__(self,id_dev="",location_dev="unknown",light=False):
        super(Hue, self).__init__(id_dev, location_dev, type_dev="Hue")
        self.light=light
         
    def to_text(self):
        array=[]
        array.append(self.id)
        array.append(self.location)
        array.append(self.type)
        array.append(self.time_resolution)
        array.append(self.light)
        return json.dumps(array)   
        
        
    def from_text(self,serial_dict):
        struct=json.loads(str(serial_dict))
        if type(struct)=='list':
            self.id=struct[0]
            self.location=struct[1]
            self.type =struct[2]
            self.time_resolution=struct[3]
            self.light =struct[4]
        else:
            self.id = struct['id_dev']
            self.location =struct['location_dev'] 
            self.type=struct['type_dev']
            self.time_resolution=struct['time_resolution']
            self.light=struct['light']
        return self    
        
    @staticmethod          
    def make_active(device):
        #Define Handlers here
        def light(message , active):
            #print("WriteRequest : ",message.payload.decode("utf-8"))
            active.dev.light=message['value'] in [True,"True","true","y"]
            active.publish()
                
        handlers=[("/device/"+device.id+"/light",light)] #[("topic1",function1),("topic2",function2)] like [("/device/"+id_dev+"/light",function)]
        #Define Job to perform periodically
        def job_to_do(active):
            while True:
                with active.locker: 
                    active.publish()
                time.sleep(active.dev.time_resolution)                   
        return ActiveDevice(device,job_to_do,handlers)
    