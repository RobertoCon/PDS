'''
Created on 06 apr 2017

@author: Conny
'''
from FunctionalLayer.TEMP import TEMP
import time
from ApplicationLayer.TimeEvent import TimeEvent

devs=TEMP().filter(lambda x : x.location=="bed" and x.type=="TempSensor" )
print("Size :",len(devs))
lambs=[]
for i in devs:
    lambs.append(lambda x: x.temperature>10)
event=TimeEvent(devs,lambs,1)




while True:
    time.sleep(5)
    
    
