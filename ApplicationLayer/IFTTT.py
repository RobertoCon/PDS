'''
Created on 23 nov 2016

@author: Conny
'''
from ApplicationLayer.Observer import Observer
class IFTTT(Observer):
    
    def __init__(self, dev,func,lamb):
        super(IFTTT, self).__init__(dev,func)
        self.lamb=lamb
         
    def notify_update(self):
        if self.lamb(self.dev):
            self.func(self,self.dev)