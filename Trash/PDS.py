'''
Created on 30 ott 2016

@author: Conny
'''

from _functools import reduce

from ApplicationLayer.ShadowBroker import ShadowBroker


class PDS(list):
    dev_type="+"
    dev_location="+"
    
    def __init__(self,shadow=None,starter=None):
        if shadow==None :
            self.shadow=ShadowBroker()
            self.shadow.listenComplex(self.dev_type, self.dev_location)
        
        if starter==None :
            super(PDS, self).__init__()
        else:
            super(PDS, self).__init__(starter)
        
    def filter(self,func):
        return type(self)(filter(func ,self))
        
    def map(self,func):
        return type(self)(map(func,self))
 
    def reduce(self,func):
        return reduce(func,self)
    
    
    def print(self):
        for i in self:
            print(i.json())
            
            
            
class HUE(PDS):
    dev_type="HUE"
    dev_location="+"
    
    def __init__(self,shadow=None,starter=None):
        super(HUE, self).__init__()
        
        if shadow==None :
            self.shadow=ShadowBroker()
            self.shadowShared=False
        else :
            self.shadow=shadow
            self.shadowShared=True
  
   
PDS.dev_location     