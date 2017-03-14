
from Device.Device import Device
from Device.ActiveDevice import ActiveDevice
import json
import time
import random

class LightSensor(Device):

    def __init__(self,id_dev="",location_dev="unknown",light=0,unit="lumen"):

        super(LightSensor, self).__init__(id_dev, location_dev, type_dev="LightSensor")
        self.light=light
        self.unit=unit
        
    def to_text(self):
        struct = {}
        struct['id_dev'] = self.id
        struct['location_dev'] = self.location
        struct['type_dev'] = self.type
        struct['light'] = self.light
        struct['unit'] = self.unit
        return json.dumps(struct)
    
    def from_text(self,serial_dict):
        struct=json.loads(str(serial_dict))
        self.id = struct['id_dev']
        self.location =struct['location_dev'] 
        self.type=struct['type_dev']
        self.light=struct['light']
        self.unit=struct['unit']
        return self
        
    @staticmethod          
    def make_active(device):
        #Define Handlers here
        handlers=[] #[("topic1",function1),("topic2",function2)] like [("/device/"+id_dev+"/light",function)]
        #Define Job to perform periodically
        def job_to_do(active):
            while True:        
                active.dev.light=random.randint(1,100)
                active.publish()
                time.sleep(10)        
        return ActiveDevice(device,job_to_do,handlers)