'''
Created on 12 mar 2017

@author: Conny
'''
import time
from Benchmark.DeviceGenerator import DeviceGenerator 
from FunctionalLayer.HUE import HUE
import random

#Init Test
gen=DeviceGenerator('''node_templates:
                                          dev:
                                            type_dev: Hue
                                            id_dev: dev
                                            location_dev: location
                                            requirements: {host: hoster}
                                            type: my.Device.Hue
                                            light: true ''')
size_gen=5
iter_gen=10
time_wait=2
list_location=['bath','bed','living']
list_host=['raspy3-A']
for i in range(iter_gen):
    gen.make(size_gen, list_location, list_host)
    print("Iter :",i,"Device size : ",len(HUE()))
    time.sleep(time_wait)

while(1):
    start_time= time.perf_counter()
    start_process = time.process_time()
    
    #Codeblock test
    x=random.choice(HUE())
    print("Id : ",x.id,"   State before : ",x.light)
    #x.setattr("light",not(x.light))
    x.light=not(x.light)
    print("Id : ",x.id,"  State after : ",x.light)
    elapsed_process = (time.process_time() - start_process)
    elapsed_time = (time.perf_counter() - start_time)
    print("Device size : ",len(HUE())," Process Time : ",elapsed_process," Time : ",elapsed_time)