'''
Created on 20 dic 2016

@author: Conny
'''

import json
from pathlib import Path
from functools import partial
from Model import Setting
import paho.mqtt.client as mqtt

def on_message(client, userdata, message, table, path):
    #print("Received message '" + str(message.payload) + "' on topic '"+ message.topic + "' with QoS " + str(message.qos))
    serial_frame=str(message.payload.decode("utf-8"))
    json_frame=json.loads(serial_frame)
    json_dev=json.loads(json_frame['device'])
    id_dev = json_dev['id']


class SharedMemory(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.table=[]
        
        self.client = mqtt.Client()
        self.client.connect(Setting.Broker_ip)
        self.client.on_message = partial(on_message, table=self.table,path=self.path)
        self.client.loop_start()        
        
        self.path = Path(Setting.path+"/Settings/").absolute()
        self.path.mkdir(parents=True, exist_ok=True)
        self.path=self.path.joinpath("data.json")
        

        if self.path.is_file() == False :
            json.dump(self.table,open(str(self.path),'w')) 
        else:
            #read it
            self.table=json.load(open(str(self.path),'r'))

            
    def create(self,key,data):
        self.table.append(key)
        json.dump(self.table,open(str(self.path),'w')) 
        self.client.publish(topic, payload, qos, retain)
    
    def read(self):
        pass
    
    def write(self,key,data):
        self.table[key]=data
        json.dump(self.table,open(str(self.path),'w'))

s=SharedMemory()
s.write("qui","asd")
print(s.table)