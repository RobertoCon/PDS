'''
Created on 23 nov 2016

@author: Conny
'''
from ApplicationLayer.ShadowBroker import ShadowBroker
import time
class TimeEvent(object):
    
    def __init__(self,devs,lambs,time):
        self.shadow=ShadowBroker()
        self.time=time
        self.status=False
        self.devs=devs
        self.lambs=lambs
        for i in devs:
            self.shadow.observer(i.id,self)

         
    def notify_update(self):
        self.status=True        
        for i in range(len(self.devs)):
            self.status=self.status and self.lambs[i](self.devs[i]) and (time.time()-self.devs[i].timestamp < self.time)
        
        if self.status:
            print("------------------")
            print("Status : ",self.status) 
            for i in range(len(self.devs)): 
                print(" Temp : ",self.devs[i].temperature,"  time : ",self.devs[i].timestamp) 

