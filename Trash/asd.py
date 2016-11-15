'''
import paho.mqtt.client as mqtt
from functools import partial
import json
import threading
import time
import random


def on_message(client, userdata, message , sensor):
        
        if message.topic=="/request/device" :
            sensor.client.publish("/response/device", sensor.json_print())

class Sensor(threading.Thread):
    
    classdocs
    
    def __init__(self,ID,location,type_obj):
        
       
        self.id=ID
        self.location=location
        self.device=type_obj
        self.temperature=random.randint(1,30)
        self.valid="1"
        threading.Thread.__init__(self)
        self.client = mqtt.Client()
        self.client.will_set("/device/"+self.id, "{\"id\":\""+self.id+"\" , \"valid\" : \"0\" }", 0, True)
        self.client.connect("192.168.1.5")
        self.client.loop_start()
        '''self.client.on_message =  partial(on_message, sensor=self)'''
        '''self.client.subscribe("/request/device", qos=0)'''
       
        ''' Attributi '''
       
       
        self.start()
        
    def run(self):
        while True:
            time.sleep(30)
            'publish something'
            self.client.publish("/device/"+self.id, self.json_print(),0,retain=True)
            self.temperature=random.randint(1,30)
    
    def json_print(self):
        data = {}
        data['id'] = self.id
        data['location'] = self.location
        data['device'] = self.device
        data['temperature'] = self.temperature
        data['valid'] = self.valid
        return json.dumps(data)
''' 
    def filter(self,func):
        self.client.publish("id/request", "" )
        self.client.on_message = partial(self.on_message, self=self)
        self.client.subscribe("/device/example", qos=0)
        counter = 0
        while counter<10:
                time.sleep(0.5)
                counter=counter+1
        self.client.unsubscribe("/device/example")
        return func('hello world')
        
