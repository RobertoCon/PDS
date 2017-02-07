'''
Created on 29 ott 2016

@author: Conny
'''

from functools import partial
from Model import Setting
import paho.mqtt.client as mqtt
from Dev.Factory import Factory
from ApplicationLayer.Observable import Observable
import json
import time
import copy
from ApplicationLayer.RemoteDevice import RemoteDevice
from concurrent.futures import ThreadPoolExecutor


          

def isTopicValid(obj,topic):
    return topic_in(obj.dev.topic(),topic)


def topic_in(a,b):
    t1=b.split("/")
    t2=a.split("/")  
    if t1[2]=="+" or  t1[2]==t2[2] :  #different topic
        if t1[3]=="+" or  t1[3]==t2[3] :
            if t1[4]=="+" or  t1[4]==t2[4] :
                return True
    return False  



def on_message(client, userdata, message , cache):
    #print("Received message '" + str(message.payload) + "' on topic '"+ message.topic + "' with QoS " + str(message.qos))
    serial_frame=str(message.payload.decode("utf-8"))
    json_frame=json.loads(serial_frame)
    json_dev=json.loads(json_frame['device'])
    id_dev = json_dev['id']
    if id_dev != None:
        for i, item in enumerate(cache):
            if id_dev==item.id_dev:
                if json_frame['state']=="online":
                    cache[i].update(json_frame['device'],json_frame['lock_id'],json_frame['state'])
                    #notify change to all observer
                    #cache[i].notify_update()
                else:
                    cache[i].state="offline"
                return
        cache.append(Observable(id_dev,Factory.decode(json.dumps(json_dev)),json_frame['lock_id'],json_frame['state']))
    
    #REMOVE OBJECT DISCONNECTED
            
class ShadowBroker(object):
    class __ShadowBroker(object):
        def __init__(self):
            #Device Pool
            self.cache=[]
            self.topics=[]
            #Mqtt connection
            self.client = mqtt.Client()
            #Comunicare che sono morto
            #self.client.will_set("/client/"+self.client._client_id+"/status","offline", 0, True)
            self.client.connect(Setting.getBrokerIp())
            self.client.on_message = partial(on_message, cache=self.cache)
            self.client.loop_start()
            #self.client.publish("/client/"+self.client._client_id+"/status","online", 0, True)
            self.executor=ThreadPoolExecutor(max_workers=1)
        def publish(self,topic,message):
            self.client.publish(topic,message,qos=0)
        

        def listen(self,topic):
            add=True
            for i in self.topics:
                if topic_in(topic,i):
                    add=False
            if add:
                self.topics.append(topic)
                self.client.subscribe(topic, qos=0)
            rm=[]
            for item in self.topics:
                if item!=topic:
                    if topic_in(item,topic):
                        rm.append(item)   
            for item in rm:
                self.topics.remove(item)
                self.client.unsubscribe(item) 
            return add
        
        def observer(self,id_dev,obs):
            for i in self.cache:
                if i.dev.id==id_dev:
                    i.observer(obs)
                    return True
            return False
        
        #utility
        def topics_print(self):
            return self.topics         
       
        
        def get_device(self,id_dev):
            for i in self.cache:
                if i.dev.id==id_dev:
                    return i.dev
            return None
        
        def get_history_of(self,id_dev):
            for i in self.cache:
                if i.dev.id==id_dev:
                    return i.get_history()
            return None
                    
        #Non so che fare
        #Read_only or local write 
        def get_subset_local(self,topic):
            cp=[]
            for i in filter(partial(isTopicValid,topic=topic),self.cache):
                x=copy.copy(i.dev)
                cp.append(x)
            return cp
        
        def get_subset_remote(self,topic):
            cp=[]
            for i in filter(partial(isTopicValid,topic=topic),self.cache):
                x=RemoteDevice(i.dev,self)
                cp.append(x)
            return cp
        
        #Autoupdate , remote writer , listener
        #def get_subset_observers(self,topic):
        #    cp=[]
        #    for i in filter(partial(isTopicValid,topic=topic),self.cache):
        #        x=i.get_observer()
        #        cp.append(x)
        #    return cp
        
        #def getShadow(self,topic):
        #    cp=[]
        #    for i in filter(partial(isTopicValid,topic=topic),self.data):
        #        x=copy.copy(i)
        #        x.setWrapper(self)
        #        cp.append(x)
        #    return cp
        
       
        #def listenType(self,dev_type):
        #    self.topics.append("/device/+/"+dev_type+"/+")
        #   self.client.subscribe("/device/+/"+dev_type+"/+", qos=0)
            
        #def listenLocation(self,dev_location):
        #    self.topics.append("/device/+/+/"+dev_location)
        #    self.client.subscribe("/device/+/+/"+dev_location, qos=0)
        def get_lock_id(self,id_dev):
            for i in self.cache:
                if i.dev.id==id_dev:
                    return i.lock_id
            return None  
        
        def lock(self,dev_id):
            #self.publish("/device/"+dev_id+"/lock",self.client._client_id)
            self.publish("/device/"+dev_id+"/lock",self.frame_request())
            while True:
                lock_id=self.get_lock_id(dev_id)
                #print("Lock request [ id : ",x.lock_id," client_id : ",self.client._client_id," ]")
                if lock_id==self.client._client_id:
                    return copy.copy(self.get_device(dev_id))
                else:
                    time.sleep(0.5)
                    
        def unlock(self,dev_id):
            #self.publish("/device/"+dev_id+"/unlock",self.client._client_id)
            self.publish("/device/"+dev_id+"/unlock",self.frame_request())
            while True:
                #x=self.getDevById(dev_id)
                lock_id=self.get_lock_id(dev_id)
                #print("Unlock request")
                if lock_id!=self.client._client_id:
                    return copy.copy(self.get_device(dev_id))
                else:
                    time.sleep(0.5)                     
      
      
      
        
                
        def write(self,dev_id,name,value,callback):
            #print("ShadowBroker Write")
            def func_write(shadow,dev_id,name,value):
                    time.sleep(5)
                    shadow.publish("/device/"+dev_id+"/"+name,shadow.frame_request(name,value))
                    #while True:
                    #    x=self.get_device(dev_id)
                    #    if getattr(x, name)==value:
                    #        return copy.copy(self.get_device(dev_id))
                    #    else:
                    #        time.sleep(0.5)
                    
            
            future = self.executor.submit(partial(func_write,self,dev_id,name,value))
            if callback != None:
                future.add_done_callback(callback)
                #print("ShadowBroker Write end return : ",future)
            return future
            #print("ShadowBroker Write end return nothing")
                    
        def frame_request(self,name="",value=""):
                struct = {}
                struct['client_id'] = self.client._client_id
                struct['state'] = "online"
                struct['name'] = name
                struct['value'] = value
                #struct['id_request'] = #Random value
                return json.dumps(struct)
            
    instance = None
    def __init__(self):
        if not ShadowBroker.instance:
            ShadowBroker.instance = ShadowBroker.__ShadowBroker()
            time.sleep(3)
    def __getattr__(self, name):
        return getattr(self.instance, name)
    def __setattr__(self, name):
        return setattr(self.instance, name)


'''
def on_message(client, userdata, message , data):
    #print("Received message '" + str(message.payload) + "' on topic '"+ message.topic + "' with QoS " + str(message.qos))
    dev = Factory.decode(json.loads(str(message.payload.decode("utf-8"))))
    if dev != None:
        for i, item in enumerate(data):
            if dev.id==item.id: 
                #data[i] = dev
                data[i].__dict__ = dev.__dict__
                return
        data.append(dev)
    else:
        id_dev=message.topic.split("/")[2]  #/device/id/type/location  remove also 
        for i, item in enumerate(data):
            if id_dev==item.id: 
                print("Remove dev id ",id_dev)
                data.remove(item)
                return
'''        
   
   
   
'''
           
def on_message(client, userdata, message , data):
    #print("Received message '" + str(message.payload) + "' on topic '"+ message.topic + "' with QoS " + str(message.qos))
    dev_id = json.loads(str(message.payload.decode("utf-8")))['id']
    if dev_id != None:
        for i, item in enumerate(data):
            if dev_id==item.id: 
                data[i].from_json(str(message.payload.decode("utf-8")))
                #notify change to all observer
                return
        data.append(Factory.decode(json.loads(str(message.payload.decode("utf-8")))))
    #else:
    #    id_dev=message.topic.split("/")[2]  #/device/id/type/location  remove also 
    #    for i, item in enumerate(data):
    #        if id_dev==item.id: 
    #            print("Remove dev id ",id_dev)
    #            data.remove(item)
    #            return
            
class ShadowBroker(object):
    class __ShadowBroker(object):
        def __init__(self):
            #Device Pool
            self.data=[]
            self.topics=[]
            #Mqtt connection
            self.client = mqtt.Client()
            #Comunicare che sono morto
            #self.client.will_set("/client/"+self.client._client_id+"/status","offline", 0, True)
            self.client.connect(Setting.Broker_ip)
            self.client.on_message = partial(on_message, data=self.data)
            self.client.loop_start()
            #self.client.publish("/client/"+self.client._client_id+"/status","online", 0, True)
        
        def publish(self,topic,message):
            self.client.publish(topic, message,qos=0)
        
        
        
        
        
        def getShadow(self,topic):
            cp=[]
            for i in filter(partial(isTopicValid,topic=topic),self.data):
                x=copy.copy(i)
                x.setWrapper(self)
                cp.append(x)
            return cp
        
        def lock(self,dev_id):
            self.publish("/device/"+dev_id+"/lock",self.client._client_id)
            while True:
                x=self.getDevById(dev_id)
                print("Lock request [ id : ",x.lock_id," client_id : ",self.client._client_id," ]")
                if x.lock_id==self.client._client_id:
                    return copy.copy(x)
                else:
                    time.sleep(0.5)
        def unlock(self,dev_id):
            self.publish("/device/"+dev_id+"/unlock",self.client._client_id)
            while True:
                x=self.getDevById(dev_id)
                print("Unlock request")
                if x.lock_id!=self.client._client_id:
                    return copy.copy(x)
                else:
                    time.sleep(0.5)
        #def listenType(self,dev_type):
        #    self.topics.append("/device/+/"+dev_type+"/+")
        #   self.client.subscribe("/device/+/"+dev_type+"/+", qos=0)
            
        #def listenLocation(self,dev_location):
        #    self.topics.append("/device/+/+/"+dev_location)
        #    self.client.subscribe("/device/+/+/"+dev_location, qos=0)
            
        def listen(self,topic):
            add=True
            for i in self.topics:
                if topic_in(topic,i):
                    add=False
            if add:
                self.topics.append(topic)
                self.client.subscribe(topic, qos=0)
            rm=[]
            for item in self.topics:
                if item!=topic:
                    if topic_in(item,topic):
                        rm.append(item)   
            for item in rm:
                self.topics.remove(item)
                self.client.unsubscribe(item) 
            if add:
                return True
                             
               
            
        def topic_print(self):
            return self.topics
        
        def getDevById(self,id_dev):
            for i in self.data:
                if i.id==id_dev:
                    return i
            return None
                    
        
        def cleanListener(self):
            for i in self.topics:
                self.client.unsubscribe(i)
                
                
        def write(self,dev_id,name,value):
            print("Write ",dev_id," ",name," ",value)
            x=self.getDevById(dev_id)
            if x.lock_id==self.client._client_id:
                    print("Safe Write ")
                    #safe write
                    self.publish("/device/"+dev_id+"/"+name,value)
                    while True:
                        x=self.getDevById(dev_id)
                        print("Write at : ",x.__dict__)
                        if x.__dict__[name]==value:
                            return copy.copy(x)
                        else:
                            time.sleep(0.5)
            else:
                    print("Unsafe Write ")
                    #unsafe write
                    self.publish("/device/"+dev_id+"/"+name,value)
                    
            
    instance = None
    def __init__(self):
        if not ShadowBroker.instance:
            ShadowBroker.instance = ShadowBroker.__ShadowBroker()
            time.sleep(3)
    def __getattr__(self, name):
        return getattr(self.instance, name)
    def __setattr__(self, name):
        return setattr(self.instance, name)
'''        