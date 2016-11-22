'''
Created on 26 ott 2016

@author: Conny
'''

from functools import partial
from Model import Setting
import paho.mqtt.client as mqtt
import threading
import json

class ActiveDevice(threading.Thread):
            
    def __init__(self,dev,runnable=None,handlers=[]):
        
        super(ActiveDevice, self).__init__()
        self.dev=dev
        self.locker=threading.RLock()
        self.lock_id=""
        self.lock_stack=[]
        self.client = mqtt.Client()
        self.client.will_set(self.dev.topic(),'{"id":"'+self.dev.id +'", "state":"offline","lock_id":"", "device": ""}', 0, True)
        def lock(client, userdata, message , act):
            with self.locker:
                self.lock_stack.append(str(message.payload.decode("utf-8")))
                if act.lock_id=="":
                    act.lock_id=self.lock_stack.pop()
                    act.publish()
                
        def unlock(client, userdata, message , act):
            with self.locker:
                for item in enumerate(self.lock_stack):
                    if str(message.payload.decode("utf-8"))==item: 
                        self.lock_stack.remove(item)
                if message.payload.decode("utf-8")==act.lock_id:
                    if len(self.lock_stack)>0 :
                        act.lock_id=self.lock_stack.pop()
                    else:
                        act.lock_id=""
                    act.publish()
                 
        def update(client, userdata, message , act):
            with self.locker:
                act.publish()
            
        self.runnable=runnable
            
        def write_wrapp(client, userdata, message , act , func):
            print("Received message '" + str(message.payload) + "' on topic '"+ message.topic + "' with QoS " + str(message.qos))
            if str(message.payload.decode("utf-8"))==act.lock_id or act.lock_id=="":
                with self.locker:
                    func(client, userdata, message,act)
               
        for i in handlers:
            self.client.message_callback_add(i[0], partial(write_wrapp,act=self,func=i[1]))
        self.client.message_callback_add("/device/"+self.dev.id+"/lock", partial(write_wrapp,act=self,func=lock)) 
        self.client.message_callback_add("/device/"+self.dev.id+"/unlock", partial(write_wrapp,act=self,func=unlock))
        self.client.message_callback_add("/device/"+self.dev.id+"/update", partial(write_wrapp,act=self,func=update)) 
        
        
        self.client.connect(Setting.Broker_ip)
        self.client.loop_start()
        self.start()
        for i in handlers:
            self.client.subscribe(i[0], qos=0)
        self.client.subscribe("/device/"+self.dev.id+"/lock", qos=0)
        self.client.subscribe("/device/"+self.dev.id+"/unlock", qos=0)
        self.client.subscribe("/device/"+self.dev.id+"/update", qos=0)
    
    def run(self):
        self.runnable(self)
        
    def publish(self):
        with self.locker:
            #self.client.publish(self.dev.topic(), self.dev.to_json(),0,retain=True)
            struct = {}
            struct['id'] = self.dev.id
            struct['state'] = "online"
            struct['device'] = self.dev.to_json()
            struct['lock_id'] = self.lock_id
            self.client.publish(self.dev.topic(),json.dumps(struct),0,retain=True)
            
            
            
            