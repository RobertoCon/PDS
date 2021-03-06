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
      
    def __init__(self,dev,runnable=None,handlers=[],broker_ip=Setting.getBrokerIp()):
        
        super(ActiveDevice, self).__init__()
        self.isAlive=True
        self.dev=dev
        self.locker=threading.RLock()
        self.lock_id=""
        self.lock_stack=[]
        self.client = mqtt.Client()
        self.client.will_set(self.dev.topic(),'["'+self.dev.id +'","offline","",""]', 0, True)
        self.runnable=runnable
        
        def lock(message , act):
            with self.locker:
                self.lock_stack.append(message['client_id'])
                if act.lock_id=="":
                    act.lock_id=self.lock_stack.pop()
                    act.publish()
                
        def unlock(message , act):
            with self.locker:
                for item in enumerate(self.lock_stack):
                    if message['client_id']==item:
                        self.lock_stack.remove(item)
                if message['client_id']==act.lock_id:
                    if len(self.lock_stack)>0 :
                        act.lock_id=self.lock_stack.pop()
                    else:
                        act.lock_id=""
                    act.publish()
                 
        def update(message , act):
            with self.locker:
                act.publish()

        def write_wrapp(client, userdata, message , act , func):
            json_frame=json.loads(str(message.payload.decode("utf-8")))
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
        for i in handlers:
            self.client.subscribe(i[0], qos=0)
        self.client.subscribe("/device/"+self.dev.id+"/lock", qos=0)
        self.client.subscribe("/device/"+self.dev.id+"/unlock", qos=0)
        self.client.subscribe("/device/"+self.dev.id+"/update", qos=0)
        
        self.start()
        
    def publish(self):
        with self.locker:
            '''struct = {}
            struct['id'] = self.dev.id
            struct['state'] = "online"
            struct['device'] = self.dev.to_text()
            struct['lock_id'] = self.lock_id
            self.client.publish(self.dev.topic(),json.dumps(struct),0,retain=True)'''
            
            struct=[]
            struct.append(self.dev.id)
            struct.append("online")
            struct.append(self.lock_id)
            struct.append(self.dev.to_text())
            
            self.client.publish(self.dev.topic(),json.dumps(struct),0,retain=True)
            
            
    
    def run(self):
        self.runnable(self)

    def terminate(self):
        with self.locker:
            self.isAlive=False
            #self.client.publish(self.dev.topic(),'{"id":"'+self.dev.id +'", "state":"offline","lock_id":"", "device": ""}', 0, True)
            self.client.publish(self.dev.topic(),'["'+self.dev.id +'","offline","",""]', 0, True)
            self.client.disconnect()
            self.client.loop_stop(True) 