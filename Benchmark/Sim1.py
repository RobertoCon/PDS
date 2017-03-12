'''
Created on 12 mar 2017

@author: Conny
'''
import time
from Benchmark.DeviceGenerator import DeviceGenerator 
from ApplicationLayer.PDS import TEMP


#Init Test
gen=DeviceGenerator()
size_gen=0
iter_gen=50
time_wait=5
list_location=['bath','bed','living']
list_host=['raspy3-A']

for i in range(iter_gen):
    gen.make(size_gen, list_location, list_host)
    time.sleep(time_wait)
    start_time= time.perf_counter()
    start_process = time.process_time()
    
    #Codeblock test
    avg=TEMP().map(lambda x : x.temperature).reduce(lambda x, y : (x+y)/2)
    
    elapsed_process = (time.process_time() - start_process)
    elapsed_time = (time.perf_counter() - start_time)
    print("Device size : ",len(TEMP())," Process Time : ",elapsed_process," Time : ",elapsed_time," AVG : ",avg)
    
    
    
    
#Result 1:
#Boot clean 20 thread
#    115 device --> 250 thread ... RuntimeError: can't start new thread
#Almost 2 thread for device ...... need to reduce it with pool or aggregator
