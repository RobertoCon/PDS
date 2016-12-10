'''
Created on 23 nov 2016

@author: Conny
'''
from ApplicationLayer.Observer import Observer
class IFTTT(Observer):
    
    def __init__(self, dev,lamb):
        from ApplicationLayer.ShadowBroker import ShadowBroker
        super(IFTTT, self).__init__(dev)
        self.lamb=lamb
         
    def notify_update(self):
        if self.lamb(self.dev):
            print("Triggered IFTTT by : ",self.dev)
            #do something