'''
Created on 31 ott 2016

@author: Conny
'''
from Device.ActiveDevice import ActiveDevice
import json
import time

class Device(object):
  
    def __init__(self ,id_dev="",location_dev="unknown",type_dev="device"):

        self.id=id_dev
        self.location=location_dev
        self.type=type_dev
       
    #Redefine how to serialize the struct
    def to_text(self):
        '''
        struct = {}
        struct['id_dev'] = self.id
        struct['location_dev'] = self.location
        struct['type_dev'] = self.type
        return json.dumps(struct)
        '''
        
        array=[]
        array.append(self.id)
        array.append(self.location)
        array.append(self.type)
        return json.dumps(array)

    '''
        array=[]
        array[0]=self.id
        array[1]=self.location
        array[2]=self.type
    '''
    
    def topic(self):
        return "/device/"+self.id+"/"+self.type+"/"+self.location
    
    def from_text(self,serial_dict):
        obj=json.loads(str(serial_dict))
        if type(obj)=='list':
            self.id=obj[0]
            self.location=obj[1]
            self.type =obj[2]
        else:
            self.id = obj['id_dev']
            self.location =obj['location_dev'] 
            self.type=obj['type_dev']
        return self
    
        '''
        struct=json.loads(str(serial_dict))
        self.id = struct['id_dev']
        self.location =struct['location_dev'] 
        self.type=struct['type_dev']
        return self
        '''
              
    @staticmethod          
    def make_active(device):
        #Define Handlers here
        
        handlers=[] #[("topic1",function1),("topic2",function2)] like [("/device/"+id_dev+"/light",function)]
        #Define Job to perform periodically
        def job_to_do(active):
            while active.isAlive:
                active.publish()
                time.sleep(10)
                
        return ActiveDevice(device,job_to_do,handlers)
    
    @staticmethod          
    def html(device):
        html=""
        #build html code 
        return html