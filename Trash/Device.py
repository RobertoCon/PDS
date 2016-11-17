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
        
        
    def json(self):  
        data = {}
        data['id'] = self.id
        data['location'] = self.location
        data['type'] = self.type
        return json.dumps(data)
    
    def topic(self):
        return "/device/"+self.id+"/"+self.type+"/"+self.location
    
   