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
            
    def __init__(self,dev,runnable=None,handlers=[],broker_ip=Setting.Broker_ip):
        
        super(ActiveDevice, self).__init__()
        self.isAlive=True
        self.dev=dev
        self.locker=threading.RLock()
        self.lock_id=""
        self.lock_stack=[]
        self.client = mqtt.Client()
        self.client.will_set(self.dev.topic(),'{"id":"'+self.dev.id +'", "state":"offline","lock_id":"", "device": ""}', 0, True)
        def lock(message , act):
            with self.locker:
                #self.lock_stack.append(str(message.payload.decode("utf-8")))
                self.lock_stack.append(message['client_id'])
                if act.lock_id=="":
                    act.lock_id=self.lock_stack.pop()
                    act.publish()
                
        def unlock(message , act):
            with self.locker:
                for item in enumerate(self.lock_stack):
                    #if str(message.payload.decode("utf-8"))==item: 
                    if message['client_id']==item:
                        
                        self.lock_stack.remove(item)
                #if message.payload.decode("utf-8")==act.lock_id:
                if message['client_id']==act.lock_id:
                    if len(self.lock_stack)>0 :
                        act.lock_id=self.lock_stack.pop()
                    else:
                        act.lock_id=""
                    act.publish()
                 
        def update(message , act):
            with self.locker:
                act.publish()
            
        self.runnable=runnable
            
        def write_wrapp(client, userdata, message , act , func):
            #print("Received message '" + str(message.payload) + "' on topic '"+ message.topic + "' with QoS " + str(message.qos))
            #json_frame['client_id']
            json_frame=json.loads(str(message.payload.decode("utf-8")))
            #if str(message.payload.decode("utf-8"))==act.lock_id or act.lock_id=="":
            if json_frame['client_id']==act.lock_id or act.lock_id=="":
                with self.locker:
                    func(json_frame,act)
               
        for i in handlers:
            self.client.message_callback_add(i[0], partial(write_wrapp,act=self,func=i[1]))
        self.client.message_callback_add("/device/"+self.dev.id+"/lock", partial(write_wrapp,act=self,func=lock)) 
        self.client.message_callback_add("/device/"+self.dev.id+"/unlock", partial(write_wrapp,act=self,func=unlock))
        self.client.message_callback_add("/device/"+self.dev.id+"/update", partial(write_wrapp,act=self,func=update)) 
        
        
        self.client.connect(broker_ip)
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
            
    def terminate(self):
        with self.locker:
            self.isAlive=False
            self.client.disconnect()
            self.client.loop_stop() 
               
            
            