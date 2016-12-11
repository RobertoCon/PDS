'''
Created on 10 dic 2016

@author: Conny
'''


class Observer(object):
        def __init__(self,dev,func):
            from ApplicationLayer.ShadowBroker import ShadowBroker
            self.dev=dev
            self.shadow=ShadowBroker()
            self.shadow.observer(dev.id,self)
            self.func()
            
        def notify_update(self):
            #do something
            #pass
            self.func()
