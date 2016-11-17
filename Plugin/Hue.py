'''
Created on 08 nov 2016

@author: Conny
'''

from Dev.Device import Device
import json

class Hue(Device):
    '''
    classdocs
    '''

    def __init__(self,id_dev,location_dev,type_dev,lock_id="",light=False):
        '''
        Constructor
        '''
        super(Hue, self).__init__(id_dev, location_dev, type_dev,lock_id)
        self.light=light
     
    def json(self):
        data = {}
        data['id'] = self.id
        data['location'] = self.location
        data['type'] = self.type
        data['light'] = self.light
        data['lock_id'] = self.lock_id
        return json.dumps(data)
    
