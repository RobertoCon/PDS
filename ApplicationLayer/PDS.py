'''
Created on 30 ott 2016

@author: Conny
'''

from _functools import reduce
from ApplicationLayer.ShadowBroker import ShadowBroker
import time

class PDS(list):

    def __init__(self,dev_id="+",dev_type="+",dev_location="+",shadow=True,starter=None):
        self.topic="/device/"+dev_id+"/"+dev_type+"/"+dev_location  
        if shadow==True :
            self.shadowBroker=ShadowBroker()
            if self.shadowBroker.listen(self.topic):
                time.sleep(2)
        else :
            self.shadowBroker=None
        self.shadow=shadow  
        if starter==None :
            super(PDS, self).__init__(self.shadowBroker.getShadow(self.topic))
        else:
            super(PDS, self).__init__(starter)
        
    def filter(self,func):
        if self.shadow==False:
            return type(self)(shadow=False,starter=filter(func ,self))
        else:
            return type(self)(shadow=False,starter=filter(func ,self.shadowBroker.getShadow(self.topic)))
            
        
    def map(self,func):
        if self.shadow==False:
            return type(self)(shadow=False,starter=map(func ,self))
        else:
            return type(self)(shadow=False,starter=map(func ,self.shadowBroker.getShadow(self.topic)))
                          
    def reduce(self,func):
        if self.shadow==False:
            return reduce(func,self,0)
        else:
            return reduce(func,self.shadowBroker.getShadow(self.topic),0)
        
    def print(self):
        for i in self:
            print(i.json())
            
            
            
class HUE(PDS):
    def __init__(self,dev_id="+",dev_type="hue",dev_location="+",shadow=True,starter=None):
        super(HUE, self).__init__(dev_id,dev_type,dev_location,shadow,starter)


            
class TEMP(PDS):
    def __init__(self,dev_id="+",dev_type="temp_sensor",dev_location="+",shadow=True,starter=None):
        super(TEMP, self).__init__(dev_id,dev_type,dev_location,shadow,starter)
        
class LIGHT(PDS):
    def __init__(self,dev_id="+",dev_type="light_sensor",dev_location="+",shadow=True,starter=None):
        super(LIGHT, self).__init__(dev_id,dev_type,dev_location,shadow,starter)
