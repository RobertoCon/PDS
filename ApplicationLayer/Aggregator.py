'''
Created on 23 nov 2016

@author: Conny
'''
from ApplicationLayer.ShadowBroker import ShadowBroker
class Aggregator(object):
    '''
    classdocs
    '''


    def __init__(self, devs,func):
        '''
        Constructor
        '''
        self.devs=devs
        self.shadow=ShadowBroker()
        self.func=func
        for dev in self.devs:
            self.shadow.observer(dev.id,self)
        
    def notify_update(self):
        self.func(self,self.devs)
      
    
      
