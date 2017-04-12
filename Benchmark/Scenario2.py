'''
Created on 12 apr 2017

@author: Conny
'''
from math import sqrt,pow
from ApplicationLayer.PDS import TEMP
from ApplicationLayer.Aggregator import Aggregator
from ApplicationLayer.TimeSeries import TimeSeries
from ApplicationLayer.Observer import Observer
import time

gps=[1.0,0.0]

tier1=[]
tier2=[]
tier3=[]

plain=[]
aggregate=[]
observed=[]

limit1= 50
limit2= 100

def distance(me,dev):
    return sqrt(pow(me[0]-dev[0], 2)+pow(me[1]-dev[1], 2))

devs=TEMP()
for dev in devs:
    dist=distance(gps,dev.gps)
    if dist<limit1:
        tier1.append((dev.id,dist))
        plain.append(dev)
    elif dist<limit2:
        tier2.append((dev.id,dist))
        aggregate.append(dev)
    else:
        tier3.append((dev.id,dist))
        observed.append(dev)
    
print("Tier 1 : " ,tier1)
print("Tier 2 : " ,tier2)
print("Tier 3 : " ,tier3)

def update(self,dev):
    print(dev.id+" ",dev.temperature)
    
def event(self,dev):
    print("Allarm > 70 for 3 times")

def avg(self,devs):
    self.avg=0
    for dev in devs:
        self.avg=(self.avg+dev.temperature)/2
        

for dev in plain:
    Observer(dev,update)
                 
virtual_dev=Aggregator(aggregate,avg)

for dev in observed:
    ts=TimeSeries(dev,event)
    ts.set_events([lambda x :  x.temperature>70,lambda x :  x.temperature>70,lambda x :  x.temperature>70])


while True:
    time.sleep(5)
    print("Avg tier 2 : ",virtual_dev.avg)





