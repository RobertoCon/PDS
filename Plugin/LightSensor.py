
from Dev.Device import Device
import json

class LightSensor(Device):
    '''
    classdocs
    '''

    def __init__(self,id_dev,location_dev,type_dev,lock_id="",light=0,unit="lumen"):
        '''
        Constructor
        '''
        super(LightSensor, self).__init__(id_dev, location_dev, type_dev,lock_id)
        self.light=light
        self.unit=unit
     
    def json(self):
        data = {}
        data['id'] = self.id
        data['location'] = self.location
        data['type'] = self.type
        data['light'] = self.light
        data['unit'] = self.unit
        data['lock_id'] = self.lock_id
        return json.dumps(data)
    
