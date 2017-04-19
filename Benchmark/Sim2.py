'''
Created on 12 mar 2017

@author: Conny
'''
import time
from FunctionalLayer.TEMP import TEMP

#Init Test

while(1):
    start_time= time.perf_counter()
    start_process = time.process_time()
    
    #Codeblock test
    time.sleep(1)
    avg=TEMP().map(lambda x : x.temperature).reduce(lambda x, y : (x+y)/2)
    
    elapsed_process = (time.process_time() - start_process)
    elapsed_time = (time.perf_counter() - start_time)
    print("Device size : ",len(TEMP())," Process Time : ",elapsed_process," Time : ",elapsed_time," AVG : ",avg)
    
    
    
    
#Result 1: