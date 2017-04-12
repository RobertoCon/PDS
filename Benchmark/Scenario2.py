'''
Created on 12 apr 2017

@author: Conny
'''
from math import sqrt,pow
from ApplicationLayer.PDS import PDS
gps=[1.0,0.0]

tier1=[]
tier2=[]
tier3=[]


limit1= 50
limit2= 100

def distance(me,dev):
    return sqrt(pow(me[0]-dev[0], 2)+pow(me[1]-dev[1], 2))

devs=PDS()
for dev in devs:
    dist=distance(gps,dev)
    if dist<limit1:
        tier1.append(dev)
    elif dist<limit2:
        tier2.append(dev)
    else:
        tier3.append(dev)
    
print("Tier 1 : " ,tier1)
print("Tier 2 : " ,tier2)
print("Tier 3 : " ,tier3)