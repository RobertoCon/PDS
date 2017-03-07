'''
Created on 23 nov 2016

@author: Conny
'''
from ApplicationLayer.ShadowBroker import ShadowBroker
class Aggregator(object):

    def __init__(self,devs,func):
        
        self.devs=devs
        self.func=func
        self.shadow=ShadowBroker()
        for dev in self.devs:
            self.shadow.observer(dev.id,self)
        self.func(self,self.devs)
    def notify_update(self):
        self.func(self,self.devs)

