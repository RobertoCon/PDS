'''
Created on 21 mar 2017

@author: Conny
'''
import time
from FunctionalLayer.RASPBERRYPI import RASPBERRYPI


while True:   
    
    avg=RASPBERRYPI().map(lambda x : x.cpus)
    print("AVG : ",avg)
    time.sleep(0.5)
    
    
    