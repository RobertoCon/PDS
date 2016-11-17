'''
Created on 31 ott 2016

@author: Conny
'''

from Dev.Device import Device
import json

class TempSensor(Device):
    '''
    classdocs
    '''

    def __init__(self,id_dev,location_dev,type_dev,lock_id="",temperature=0,unit="celsius"):
        '''
        Constructor
        '''
        super(TempSensor, self).__init__(id_dev, location_dev, type_dev,lock_id)
        self.temperature=temperature
        self.unit=unit
     
    def json(self):
        data = {}
        data['id'] = self.id
        data['location'] = self.location
        data['type'] = self.type
        data['temperature'] = self.temperature
        data['unit'] = self.unit
        data['lock_id'] = self.lock_id
        return json.dumps(data)
    
