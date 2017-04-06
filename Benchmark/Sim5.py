'''
Created on 21 mar 2017

@author: Conny
'''

import time
from Benchmark.DeviceGenerator import DeviceGenerator
import paho.mqtt.client as mqtt
from functools import partial
import threading
import psutil,os
from _functools import reduce
from Model import Setting


def on_message(client, userdata, message,counter):
        #print("Received '" +"'   message  '"+ str(message.payload) + "' on topic '"+ message.topic + "' with QoS " + str(message.qos))
        counter.add(len(str(message.payload)))
        
    
class Counter(object):
    def __init__(self):
        self.counter=0
        self.msg=0
        self.locker=threading.RLock()

    def add(self,int_num):
        with self.locker:
            self.counter=self.counter+int_num
            self.msg=self.msg+1
            return self.counter
    
    def get_byte(self):
        with self.locker:
            return self.counter
    
    def get_msg(self):
        with self.locker:
            return self.msg
    
    def zero(self):
        with self.locker:
            self.counter=0
            self.msg=0
            
            
#Init Test
gen=DeviceGenerator()
c=Counter()
client = mqtt.Client()
client.connect(Setting.getBrokerIp())
client.loop_start()
client.on_message = partial(on_message,counter=c)

size_gen=1
time_wait=5
list_location=['bathroom','bedroom','living','kitchen','closet','box']
time_resolution=[0,0.0005,0.001,0.01,0.02,0.03,0.04,0.05,0.06,0.07,0.08,0.09,0.1,0.2,0.5,1]
for i in range(len(time_resolution)):
    print("------         Test :",i," with resolution :",time_resolution[i])
    model_dev, id_dev=gen.make(size_gen, list_location, ['raspy3-A'],time_resolution[i])
    time.sleep(time_wait)
    client.subscribe("/device/"+id_dev+"/+/+", qos=0)
    n=0
    speed=0
    msg=0
    avg=0
    while n<10:
        c.zero()
        time.sleep(1)
        avg=avg+reduce(lambda x,y:(x+y)/2,psutil.cpu_percent(interval=1, percpu=True),0)
        msg=msg+c.get_msg()
        speed=speed+c.get_byte()*8/(1024*1024)
        print("Speed : ",c.get_byte()*8/(1024*1024)," MBit/s   ---   Msg : ",c.get_msg()," msg/s")
        n=n+1
        c.zero()
    
    
    gen.destroy(id_dev, model_dev)
    client.unsubscribe("/device/"+id_dev+"/+/+")
    c.zero()
    print("Speed : ",speed/10," MBit/s   ---   Msg : ",msg/10," msg/s   ----  Cpu :",avg/10)
    time.sleep(time_wait)
    
    
    
    
    

    
    
    