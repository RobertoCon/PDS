
from Dev.Device import Device
from Dev.ActiveDevice import ActiveDevice
import json
import time
import random

class LightSensor(Device):

    def __init__(self,id_dev="",location_dev="unknown",light=0,unit="lumen"):

        super(LightSensor, self).__init__(id_dev, location_dev, type_dev="LightSensor")
        self.light=light
        self.unit=unit
     
    #redefine how to serialize the struct
    def to_json(self):
        struct = {}
        struct['id'] = self.id
        struct['location'] = self.location
        struct['type'] = self.type
        struct['light'] = self.light
        struct['unit'] = self.unit
        return json.dumps(struct)
        
    def from_json(self,serial_dict):
        struct=json.loads(str(serial_dict))
        self.id = struct['id']
        self.location =struct['location'] 
        self.type=struct['type']
        self.light=struct['light']
        self.unit=struct['unit']
        return self
        
    @staticmethod          
    def make_active(device,broker_ip=""):
        #Define Handlers here
        handlers=[] #[("topic1",function1),("topic2",function2)] like [("/device/"+id_dev+"/light",function)]
        #Define Job to perform periodically
        def job_to_do(active):
            while True:        
                active.dev.light=random.randint(1,100)
                active.publish()
                time.sleep(10)        
        return ActiveDevice(device,job_to_do,handlers)