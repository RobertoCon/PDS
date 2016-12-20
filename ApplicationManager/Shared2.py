'''
Created on 20 dic 2016

@author: Conny
'''

import json
from pathlib import Path
from functools import partial
from Model import Setting
import paho.mqtt.client as mqtt

def on_message(client, userdata, message, table):
    #print("Received message '" + str(message.payload) + "' on topic '"+ message.topic + "' with QoS " + str(message.qos))
    serial_frame=str(message.payload.decode("utf-8"))
    json_frame=json.loads(serial_frame)
    key=json_frame['key']
    data=json_frame['data']
    table[key]=data


class SharedMemory(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.table={}
        
        self.client = mqtt.Client()
        self.client.connect(Setting.Broker_ip)
        self.client.on_message = partial(on_message, table=self.table)
        self.client.loop_start()        
        self.client.subscribe("/application/shared/+", qos=0)
  
            
    def write(self,key,data):
        self.table[key]=data
        message={}
        message['key']=key
        message['data']=data
        self.client.publish("/application/shared/"+key, json.dump(message), 0, True)
    
    def read(self,key):
        return self.table.get(key)

s=SharedMemory()
print(s.table)