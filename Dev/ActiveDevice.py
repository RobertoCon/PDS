'''
Created on 26 ott 2016

@author: Conny
'''
import paho.mqtt.client as mqtt
from functools import partial
import threading
from Model import Setting



class ActiveDevice(threading.Thread):
    '''
    classdocs
    '''
    
            
    def __init__(self,dev,runnable=None,handlers=[]):
        '''
        Constructor
        '''
        #threading.Thread.__init__(self)
        super(ActiveDevice, self).__init__()
        self.dev=dev
        self.lock = threading.Lock()
        self.client = mqtt.Client()
        self.client.will_set(self.dev.topic(),None, 0, True)
        def lock(client, userdata, message , act):
            print("Lock request by : ",message.payload)
            act.lock.acquire()
            act.dev.lock_id=str(message.payload.decode("utf-8"))
            act.publish()
        def unlock(client, userdata, message , act):
            print("Unlock request by : ",message.payload)
            if message.payload.decode("utf-8")==act.dev.lock_id:
                act.dev.lock_id=""
                act.publish()
                act.lock.release()
        def update(client, userdata, message , act):
            print("Update request by : ",message.payload)
            act.publish()
        self.runnable=runnable
        for i in handlers:
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
            