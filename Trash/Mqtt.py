'''
Created on 14 ott 2016

@author: Conny
'''
import paho.mqtt.client as mqtt
from functools import partial
import time
import json
from attrdict.dictionary import AttrDict

class Mqtt(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.client = mqtt.Client()
        self.client.connect("192.168.1.5")
        self.client.loop_start()
        self.data = []
        self.client.on_message = partial(on_message, data=self.data)
        self.client.subscribe("/device/+", qos=0)
       
    def getDevices(self):
        '''self.data = []
        self.client.publish( "/request/device", "")
        self.client.on_message = partial(on_message, data=self.data)
        self.client.subscribe("/response/device", qos=0)
        time.sleep(0.3)
        self.client.unsubscribe("/device/example")'''
        return self.data.copy()
    
  
def on_message(client, userdata, message , data):
    new=AttrDict(json.loads(str(message.payload.decode("utf-8"))))
    if new.valid=="0":
        for i, item in enumerate(data):
            if new.id==item.id: 
                print("Removed " ,new.id)
                data.remove(item)
                return
    else:
        for i, item in enumerate(data):
            if new.id==item.id: 
                new.pop("valid", None)
                data[i] = new
                return
        data.append(new)



'''
    Parte uguale per entrambi i job
    
    mqttc = mqtt.Client()
    mqttc.connect("192.168.1.9")
    mqttc.loop_start()
'''


'''
    Parte publisher

while True:
    temp=randint(0,100)
    print (" Temp : ",temp)
    mqttc.publish("device/temperature", temp )
    time.sleep(1)
'''   
    
'''
    Parte subscriber
'''
'''
def on_message(client, userdata, message):
    print("Received message '" + str(message.payload) + "' on topic '"
        + message.topic + "' with QoS " + str(message.qos))



mqttc.on_message = on_message   
mqttc.subscribe("/device/example", qos=0)
while True:
    time.sleep(0.5)
    
'''