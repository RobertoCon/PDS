'''
Created on 31 ott 2016

@author: Conny
'''
from Dev.ActiveDevice import ActiveDevice
import json
import time

class Device(object):
  
    def __init__(self ,id_dev="",location_dev="unknown",type_dev="device"):

        self.id=id_dev
        self.location=location_dev
        self.type=type_dev
       
    #Redefine how to serialize the struct
    def to_json(self):
        struct = {}
        struct['id'] = self.id
        struct['location'] = self.location
        struct['type'] = self.type
        return json.dumps(struct)
    
    def topic(self):
        return "/device/"+self.id+"/"+self.type+"/"+self.location
 
    def from_json(self,serial_dict):
        struct=json.loads(str(serial_dict))
        self.id = struct['id']
        self.location =struct['location'] 
        self.type=struct['type']
        return self
    
    def from_yaml(self,serial_dict):
        struct=json.loads(str(serial_dict))
        self.id = struct['id']
        self.location =struct['location'] 
        self.type=struct['type']
        return self
    
              
    @staticmethod          
    def make_active(device):
        #Define Handlers here
        
        handlers=[] #[("topic1",function1),("topic2",function2)] like [("/device/"+id_dev+"/light",function)]
        #Define Job to perform periodically
        def job_to_do(active):
            while True:
                active.publish()
                time.sleep(10)
                
        return ActiveDevice(device,job_to_do,handlers)
           
'''

Created on 31 ott 2016

@author: Conny

import json

class Device(object):
    
    classdocs
    
    def __init__(self ,id_dev ,location_dev ,type_dev,lock_id=""):
        
        Constructor
        
        self.id=id_dev
        self.location=location_dev
        self.type=type_dev
        self.lock_id=lock_id
        
        
       
    def json(self):  
        data = {}
        data['id'] = self.id
        data['location'] = self.location
        data['type'] = self.type
        data['lock_id'] = self.lock_id
        return json.dumps(data)
    
    def topic(self):
        return "/device/"+self.id+"/"+self.type+"/"+self.location
    
    def __setattr__(self, name, value):
        if name!="lock_id":
            if self.wrapper:
                    self.shadowBroker.write(self.id,name,value)
                    object.__setattr__(self, name, value)
                    return
        object.__setattr__(self, name, value)
        
    def lock(self):
        if self.wrapper:
                res=self.shadowBroker.lock(self.id)
                self.lock_id=res.lock_id
        return None
    def unlock(self):
        if self.wrapper:
                res=self.shadowBroker.unlock(self.id)
                self.lock_id=res.lock_id
        return None
    def setWrapper(self,shadowBroker):
        self.shadowBroker=shadowBroker
        self.wrapper=True
'''