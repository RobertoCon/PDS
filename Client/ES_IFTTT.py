'''
Created on 13 dic 2016

@author: Conny
'''
from FunctionalLayer.TEMP import TEMP
from ApplicationLayer.IFTTT import IFTTT
import time

devs=TEMP().filter(lambda x : x.location=="bed")#.filter(lambda x : x.unit=="Lumen")
observed=devs[0]

def event_handler(self,dev):
    print("Event happened : ",dev.timestamp)

ift=IFTTT(observed,event_handler,lambda x : x.temperature > 50)

while True:
    time.sleep(5)
    
    