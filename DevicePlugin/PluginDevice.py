'''
Created on 17 nov 2016

@author: Conny
'''

from Device.Device import Device
#from Device.ActiveDevice import ActiveDevice
from Device.ActiveDeviceOnSingleMQTT import ActiveDevice
import json
import time

class PluginDevice(Device):

        def __init__(self,id_dev="",location_dev="unknown"):   #plus other attribute
            
            super(PluginDevice, self).__init__(id_dev, location_dev, type_dev="PluginDevice")
            self.timestamp=time.time()
            #Set not base attribute
         
        def to_text(self):
            array=[]
            array.append(self.id)
            array.append(self.location)
            array.append(self.type)
            array.append(self.time_resolution)
            array.append(self.timestamp)
            return json.dumps(array)
        
        def from_text(self,serial_dict):
            obj=json.loads(str(serial_dict))
            if type(obj)=='list':
                self.id=obj[0]
                self.location=obj[1]
                self.type =obj[2]
                self.time_resolution=obj[3]
                self.timestamp=obj[4]
            else:
                self.id = obj['id_dev']
                self.location =obj['location_dev'] 
                self.type=obj['type_dev']
                self.time_resolution=obj['time_resolution']
                self.timestamp=obj['timestamp']
            return self
    
              
        @staticmethod          
        def make_active(device):
            #Define Handlers here
                
            handlers=[] #[("topic1",function1),("topic2",function2)] like [("/device/"+id_dev+"/light",function)]
            #Define Job to perform periodically
            def job_to_do(active):
                while True:
                    with active.locker:
                        #do something
                        active.publish()
                time.sleep(active.dev.time_resolution)      
            return ActiveDevice(device,job_to_do,handlers)
        
    