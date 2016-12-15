'''
Created on 13 dic 2016

@author: Conny
'''
from ApplicationLayer.PDS import LIGHT
from ApplicationLayer.IFTTT import IFTTT
import time

devs=LIGHT().filter(lambda x : x.location=="bedroom").filter(lambda x : x.unit=="Lumen")
observed=devs[0]

def event_handler(self,dev):
    print("Event happened")

ift=IFTTT(observed,lambda x : x.light>50)

while True:
    time.sleep(5)
    
    