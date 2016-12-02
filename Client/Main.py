'''
Created on 01 nov 2016

@author: Conny
'''
from ApplicationLayer.PDS import PDS,TEMP,HUE,LIGHT
import time
from ApplicationLayer.IFTTT import IFTTT
from ApplicationLayer.TimeSeries import TimeSeries
from ApplicationLayer.ShadowBroker import ShadowBroker
from ApplicationLayer.Aggregator import Aggregator


q=LIGHT(remote=True)
q.print()
#z=IFTTT(q[0],lambda x : x.light>50,ShadowBroker())
#w=TimeSeries(q[0],ShadowBroker())
#w.set_events([lambda x :  x.light<33,lambda x : x.light>=33 and x.light<66,lambda x : x.light>=67 and x.light<=100])
def avg(self,devs):
    avg=0
    for dev in devs:
        avg=(avg+dev.light)/2
        print("new average : ",avg)  
e=Aggregator([q[0],q[1],q[2]],avg,ShadowBroker())

while True:
    time.sleep(1)
    
'''
#x=LIGHT()
#x.print()
print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
y=LIGHT().filter(lambda x : x.location=="bedroom").map(lambda x:x.light).reduce(lambda x,y:(x+y)/2)
print(y)
x=HUE(remote=True).lock()

#x[0].lock()
x.print()
x[0].light=False
x.print()
#time.sleep(30)
print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
x.print()
#x[0].unlock()
x.unlock()
#x=HUE().lock()
x=HUE()
x.print()
'''