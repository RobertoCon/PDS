'''
Created on 12 mar 2017

@author: Conny
'''
import time
from Benchmark.DeviceGenerator import DeviceGenerator 
from FunctionalLayer.TEMP import TEMP


#Init Test
gen=DeviceGenerator()
size_gen=1
iter_gen=10
time_wait=20
list_location=['bathroom','bedroom','living','kitchen','closet','box']

for i in range(iter_gen):
    gen.make(size_gen, list_location, ['raspy3-A'])
    gen.make(size_gen, list_location, ['raspy2-A'])
    gen.make(size_gen, list_location, ['raspy0-A'])
    gen.make(size_gen, list_location, ['raspy0-B'])
    gen.make(size_gen, list_location, ['raspy0-C'])
    gen.make(size_gen, list_location, ['raspy1B-A'])
    gen.make(size_gen, list_location, ['raspy1B-B'])
    gen.make(size_gen, list_location, ['raspy1Bp-A'])
    time.sleep(time_wait)
    print("----------------        Iter :",i,"       Device size : ",len(TEMP()))
    start_time= time.perf_counter()
    start_process = time.process_time()
    
    #Codeblock test
    avg=TEMP().map(lambda x : x.temperature).reduce(lambda x, y : (x+y)/2)
    
    elapsed_process = (time.process_time() - start_process)
    elapsed_time = (time.perf_counter() - start_time)
    print("Device size : ",len(TEMP())," Process Time : ",elapsed_process," Time : ",elapsed_time," AVG : ",avg)
    time.sleep(5)
    
#Result 1:
