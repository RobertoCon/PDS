'''
Created on 13 dic 2016

@author: Conny
'''

from ApplicationLayer.PDS import LIGHT
from ApplicationLayer.Aggregator import Aggregator
import time

devs=LIGHT().filter(lambda x : x.location=="bedroom").filter(lambda x : x.unit=="Lumen")

def avg(self,devs):
    self.avg=0
    for dev in devs:
        self.avg=(self.avg+dev.light)/2
                 
virtual_dev=Aggregator(devs,avg)

while True:
    time.sleep(5)
    print("Average light : ",virtual_dev.avg)
    
    