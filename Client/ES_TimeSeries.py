'''
Created on 13 dic 2016

@author: Conny
'''

from FunctionalLayer.LIGHT import LIGHT
from ApplicationLayer.TimeSeries import TimeSeries
import time

devs=LIGHT().filter(lambda x : x.location=="bedroom").filter(lambda x : x.unit=="Lumen")
observed=devs[0]

def event_handler(self,dev):
    print("Event happened")

ts=TimeSeries(observed,event_handler)
ts.set_events([lambda x :  x.light>20,lambda x : x.light>=40])


while True:
    time.sleep(5)
    
    