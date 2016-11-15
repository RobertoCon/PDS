'''
Created on 26 ott 2016

@author: Conny
'''
import paho.mqtt.client as mqtt
import json
import functools
import threading
import time
from attrdict.dictionary import AttrDict
from Model import Model,Setting

'''
def on_message(client, userdata, message , active_object):
        'print("Received message '" + str(message.payload) + "' on topic '"+ message.topic + "' with QoS " + str(message.qos))'
        if message.topic=="/request/device" :
            sensor.client.publish("/response/device", sensor.json_print())
'''
class ActiveDevice(threading.Thread):
    '''
    classdocs
    '''
    def __init__(self,struct,runnable,handler):
        '''
        Constructor
        '''
        threading.Thread.__init__(self)
        self.__dict__={**self.__dict__, **struct}
        self.struct=struct
        self.runnable=runnable
        self.handler=handler
        self.valid="0"
        
    def run(self):
        '''
        self.client = mqtt.Client()
        self.client.will_set("/device/"+self.id, "{\"id\":\""+self.id+"\" , \"valid\" : \"0\" }", 0, True)
        self.client.connect(Setting.Broker_ip)
        self.client.loop_start()
        self.valid="1"
        '''
        #subscrive to topic 
        #self.client.on_message =  functools.partial(self.handler, active_object=self)
        #self.client.subscribe("/request/device", qos=0)
        
        #start active object
        self.runnable(self)
            #'publish something'
            #self.client.publish("/device/"+self.id, self.json_print(),0,retain=True)
            #self.temperature=random.randint(1,30)
        #Subscrive to something    
        
    
    def json(self):
        bigdict=self.__dict__
        wanted_keys =self.struct
        x=AttrDict((k, bigdict[k]) for k in wanted_keys if k in bigdict)
        return json.dumps(x)


def jobToDo(self):
    while True:
        print(self.json())
        time.sleep(10)
    

x=ActiveDevice(Model.structure.device.sensor_temp.struct,jobToDo,None)
x.id="pippo"
x.start()