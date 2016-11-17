'''
Created on 26 ott 2016

@author: Conny
'''

from functools import partial
import threading

from Model import Setting
import paho.mqtt.client as mqtt


class ActiveDevice(threading.Thread):
            
    def __init__(self,dev,runnable=None,handlers=[]):
        
        super(ActiveDevice, self).__init__()
        self.dev=dev
        self.lock_stack=[]
        self.client = mqtt.Client()
        #self.client.will_set(self.dev.topic(),"asd", 0, True)
        def lock(client, userdata, message , act):
            print("Lock request by : ",message.payload)
            
            self.lock_stack.append(str(message.payload.decode("utf-8")))
            if act.dev.lock_id=="":
                act.dev.lock_id=self.lock_stack.pop()
                act.publish()
                
        def unlock(client, userdata, message , act):
            print("Unlock request by : ",message.payload)
            for i, item in enumerate(self.lock_stack):
                if str(message.payload.decode("utf-8"))==item: 
                    self.lock_stack.remove(item)
            if message.payload.decode("utf-8")==act.dev.lock_id:
                if len(self.lock_stack)>0 :
                    act.dev.lock_id=self.lock_stack.pop()
                else:
                    act.dev.lock_id=""
                act.publish()
        def update(client, userdata, message , act):
            print("Update request by : ",message.payload)
            act.publish()
        self.runnable=runnable
            
        def write_wrapp(client, userdata, message , act , func):
            if str(message.payload.decode("utf-8"))==act.dev.lock_id or act.dev.lock_id=="":
                func(client, userdata, message,act)
               
        for i in handlers:
            #self.client.message_callback_add(i[0], partial(write_wrapp,act=self,func=i[1]))
            self.client.message_callback_add(i[0], partial(i[1],act=self))
        self.client.message_callback_add("/device/"+self.dev.id+"/lock", partial(lock,act=self)) 
        self.client.message_callback_add("/device/"+self.dev.id+"/unlock", partial(unlock,act=self))
        self.client.message_callback_add("/device/"+self.dev.id+"/update", partial(update,act=self)) 
        
        
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
        print("Publish : ",self.dev.json())
        self.client.publish(self.dev.topic(), self.dev.json(),0,retain=True)
        
            