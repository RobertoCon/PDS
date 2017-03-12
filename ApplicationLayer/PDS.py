'''
Created on 30 ott 2016

@author: Conny
'''

from _functools import reduce
from ApplicationLayer.ShadowBroker import ShadowBroker
import time

class PDS(list):
    def __init__(self,dev_id="+",dev_type="+",dev_location="+",shadow=True,starter=None,remote=True):
        self.topic="/device/"+dev_id+"/"+dev_type+"/"+dev_location  
        self.remote=remote
        if shadow==True :
            self.shadowBroker=ShadowBroker()
            if self.shadowBroker.listen(self.topic):
                time.sleep(2)
        else :
            self.shadowBroker=None
        self.shadow=shadow  
        if starter==None :
            #if self.remote:
                super(PDS, self).__init__(self.shadowBroker.get_subset_remote(self.topic))
            #else:
                #super(PDS, self).__init__(self.shadowBroker.get_subset_local(self.topic))
        else:
            super(PDS, self).__init__(starter)
        
    def filter(self,func):
            return type(self)(shadow=False,starter=filter(func ,self),remote=self.remote)   
        
    def map(self,func):
            return type(self)(shadow=False,starter=map(func ,self),remote=self.remote)
        
    def reduce(self,func):
            return reduce(func,self,0)
        
    def print(self):
        for i in self:
            print(i.to_json())
            
    def lock(self):
        if self.remote:
            for i in self:
                i.lock() 
        return self    

            
    def unlock(self): 
        if self.remote: 
            for i in self:
                i.unlock()
        return self     
            
class HUE(PDS):
    def __init__(self,dev_id="+",dev_type="Hue",dev_location="+",shadow=True,starter=None,remote=True):
        super(HUE, self).__init__(dev_id,dev_type,dev_location,shadow,starter,remote)
            
class TEMP(PDS):
    def __init__(self,dev_id="+",dev_type="TempSensor",dev_location="+",shadow=True,starter=None,remote=True):
        super(TEMP, self).__init__(dev_id,dev_type,dev_location,shadow,starter,remote)
        
class LIGHT(PDS):
    def __init__(self,dev_id="+",dev_type="LightSensor",dev_location="+",shadow=True,starter=None,remote=True):
        super(LIGHT, self).__init__(dev_id,dev_type,dev_location,shadow,starter,remote)