'''
Created on 31 ott 2016

@author: Conny
'''

from Device.Device import Device
from Device.ActiveDevice import ActiveDevice
import json
import time
import random

class TempSensor(Device):

    def __init__(self,id_dev="",location_dev="unknown",time_resolution=1,temperature=0,unit="celsius"):
        super(TempSensor, self).__init__(id_dev, location_dev, type_dev="TempSensor",time_resolution=time_resolution)
        self.temperature=temperature
        self.unit=unit
    
    def to_text(self):
        '''struct = {}
        struct['id_dev'] = self.id
        struct['location_dev'] = self.location
        struct['type_dev'] = self.type
        struct['temperature'] = self.temperature
        struct['unit'] = self.unit
        return json.dumps(struct)'''
        
        array=[]
        array.append(self.id)
        array.append(self.location)
        array.append(self.type)
        array.append(self.time_resolution)
        array.append(self.temperature)
        array.append(self.unit)
        return json.dumps(array)

    def from_text(self,serial_dict):
        '''
        struct=json.loads(str(serial_dict))
        self.id = struct['id_dev']
        self.location =struct['location_dev'] 
        self.type=struct['type_dev']
        self.temperature=struct['temperature']
        self.unit=struct['unit']
        return self 
    '''
    
        struct=json.loads(str(serial_dict))
        if type(struct)=='list':
            self.id=struct[0]
            self.location=struct[1]
            self.type =struct[2]
            self.time_resolution=struct[3]
            self.temperature =struct[4]
            self.unit =struct[5]
        else:
            self.id = struct['id_dev']
            self.location =struct['location_dev'] 
            self.type=struct['type_dev']
            self.time_resolution=struct['time_resolution']
            self.temperature=struct['temperature']
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
                    active.dev.temperature=random.randint(1,100) #Read temp somewhere
                    active.publish()
                time.sleep(active.dev.time_resolution)
                
        return ActiveDevice(device,job_to_do,handlers)
    
    @staticmethod          
    def html(device):
        return 'code'
    