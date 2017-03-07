'''
Created on 10 dic 2016

@author: Conny
'''
from ApplicationLayer.ShadowBroker import ShadowBroker

class Observer(object):
        def __init__(self,dev,func):
            
            self.dev=dev
            self.func=func
            self.shadow=ShadowBroker()
            self.shadow.observer(self.dev.id,self)
        def notify_update(self):
            self.func(self,self.dev)