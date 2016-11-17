'''
Created on 31 ott 2016

@author: Conny
'''
import json


class Device(object):
    '''
    classdocs
    '''
    def __init__(self ,id_dev ,location_dev ,type_dev):
        '''
        Constructor
        '''
        self.id=id_dev
        self.location=location_dev
        self.type=type_dev
        self.wrapper=False
        
    def json(self):  
        data = {}
        data['id'] = self.id
        data['location'] = self.location
        data['type'] = self.type
        return json.dumps(data)
    
    def topic(self):
        return "/device/"+self.id+"/"+self.type+"/"+self.location
    
    def __setattr__(self, name, value):
        if self.wrapper:
                self.shadowBroker.publish("/device/"+self.id+"/"+name,value)# your __setattr__ implementation here
                return
        object.__setattr__(self, name, value)
    
    def wrapper(self,shadowBroker):
        self.shadowBroker=shadowBroker
        self.wrapper=True
        
'''        
super(type(self), self).__init__(id_dev, location_dev, type_dev)
 
class Wrapper(Device):
    __initialized = False
    def __init__(self, value):
        self.value = value
        self.__initialized = True

    def __setattr__(self, name, value):
        if self.__initialized:
            # your __setattr__ implementation here
        else:
            object.__setattr__(self, name, value)
'''