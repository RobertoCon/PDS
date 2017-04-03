
from Device.Device import Device
#from Device.ActiveDevice import ActiveDevice
from Device.ActiveDeviceOnSingleMQTT import ActiveDevice
import json
import time
import random

class LightSensor(Device):

    def __init__(self,id_dev="",location_dev="unknown",light=0,unit="lumen"):

        super(LightSensor, self).__init__(id_dev, location_dev, type_dev="LightSensor")
        self.light=light
        self.unit=unit
        self.timestamp=time.time()
        
    def to_text(self):
        array=[]
        array.append(self.id)
        array.append(self.location)
        array.append(self.type)
        array.append(self.time_resolution)
        array.append(self.timestamp)
        array.append(self.light)
        array.append(self.unit)
        return json.dumps(array)
    
    def from_text(self,serial_dict):
        struct=json.loads(str(serial_dict))
        if type(struct)=='list':
            self.id=struct[0]
            self.location=struct[1]
            self.type =struct[2]
            self.time_resolution=struct[3]
            self.timestamp=struct[4]
            self.light =struct[5]
            self.unit =struct[6]
        else:
            self.id = struct['id_dev']
            self.location =struct['location_dev'] 
            self.type=struct['type_dev']
            self.time_resolution=struct['time_resolution']
            self.timestamp=struct['timestamp']
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
                with active.locker:       
                    active.dev.light=random.randint(1,100)
                    active.publish()
                time.sleep(active.dev.time_resolution)        
        return ActiveDevice(device,job_to_do,handlers)
    
    @staticmethod          
    def html(device):
        return 'code'