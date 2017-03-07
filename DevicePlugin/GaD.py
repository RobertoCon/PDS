'''
Created on 16 dic 2016

@author: Conny
'''

from Device.Device import Device
#from Device.ActiveDevice import ActiveDevice
import json


class GaD(Device):

    def __init__(self,id_dev="",location_dev="unknown"):
        super(GaD, self).__init__(id_dev, location_dev, type_dev="GaD")
        self.attr1=0
         
    #redefine how to serialize the struct
    def to_text(self):
        struct = {}
        struct['id_dev'] = self.id
        struct['location_dev'] = self.location
        struct['type_dev'] = self.type
        struct['attr1'] = self.attr1
        return json.dumps(struct)
        
    def from_text(self,serial_dict):
        struct=json.loads(str(serial_dict))
        self.id = struct['id_dev']
        self.location =struct['location_dev'] 
        self.type=struct['attr1']
        return self
'''    
    @staticmethod          
    def make_active(device,broker_ip=""):
        #Define Handlers here
            #handlers=[("topic1",function1),("topic2",function2)] like [("/device/"+id_dev+"/light",function)]
        #Define Job to perform periodically
        def job_to_do(active):
            while True:
                #do something
                active.publish()
                time.sleep(10)            
        return ActiveDevice(device,job_to_do,handlers)
'''