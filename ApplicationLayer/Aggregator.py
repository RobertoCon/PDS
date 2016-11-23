'''
Created on 23 nov 2016

@author: Conny
'''
from ApplicationLayer.Observable import Observer
class Aggregator(Observer):
    '''
    classdocs
    '''


    def __init__(self, devs,func,shadow):
        '''
        Constructor
        '''
        self.devs=devs
        self.shadow=shadow
        self.func=func
        for dev in self.devs:
            self.shadow.observer(dev.id,self)
        
    def notify_update(self):
        self.func(self,self.devs)
      
    
      
