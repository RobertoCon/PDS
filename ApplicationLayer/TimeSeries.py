'''
Created on 23 nov 2016

@author: Conny
'''
from ApplicationLayer.Observable import Observer

class TimeSeries(Observer):
    
    def __init__(self,dev,shadow):
        super(TimeSeries, self).__init__(dev,shadow)
        self.lamb=[]
        self.history=[]
    def set_events(self,events):
        for event in events:
                self.history.append(0)
                self.lamb.append(event)
               
         
    def notify_update(self):
       
        for i in reversed(range(len(self.history))):
            if i==0:
                if self.lamb[i](self.dev):
                    self.history[i]=1
                else:
                    self.history[i]=0
            else:
                if self.lamb[i](self.dev) and self.history[i-1]==1:
                    self.history[i]=1
                else:
                    self.history[i]=0
            
        print("Device : ",self.dev.to_json()," history : ",self.history )
        if self.history[len(self.history)-1]:
            #Trigger
            print("Triggered Time Series")  