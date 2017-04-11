'''
Created on 20 dic 2016

@author: Conny
'''

import json
from functools import partial
from Model import Setting
import paho.mqtt.client as mqtt
import time
import threading


def on_message(client, userdata, message, obj):
    serial_frame=str(message.payload.decode("utf-8"))
    json_frame=json.loads(serial_frame)
    key=json_frame['key']
    obj.locker.acquire()
    obj.table[key]=json.loads(json_frame['data'])
    obj.locker.release()

class SharedMemory(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.locker=threading.RLock()
        self.table={}
        
        self.client = mqtt.Client()
        self.client.connect(Setting.getBrokerIp())
        self.client.on_message = partial(on_message, obj=self)
        self.client.loop_start()        
        self.client.subscribe("/application/shared/+", qos=0)
        time.sleep(1)
  
            
    def write(self,key,data):
        self.locker.acquire()
        self.table[key]=data
        message={}
        message['key']=key
        message['data']=data
        self.client.publish("/application/shared/"+key, json.dumps(message), 0, True)
        self.locker.release()
    
    def read(self,key):
        self.locker.acquire()
        data=self.table.get(key)
        self.locker.release()
        return data

#s=SharedMemory()
#print(s.read("app1")["k1"])
#print(s.table)