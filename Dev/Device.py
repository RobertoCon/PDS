'''
Created on 31 ott 2016

@author: Conny
'''
import json

class Device(object):
    '''
    classdocs
    '''
    wrapper=False
    def __init__(self ,id_dev ,location_dev ,type_dev,lock_id=""):
        '''
        Constructor
        '''
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
                    self.shadowBroker.publish("/device/"+self.id+"/"+name,value)# your __setattr__ implementation here
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