'''
Created on 29 ott 2016

@author: Conny
'''

from functools import partial
from Model import Setting
import paho.mqtt.client as mqtt
from Dev.Factory import Factory
import json
import time
import copy

def isTopicValid(obj,topic):
    return topic_in(obj.topic(),topic)
    
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
            
class ShadowBroker(object):
    class __ShadowBroker(object):
        def __init__(self):
            #Device Pool
            self.data=[]
            self.topics=[]
            #Mqtt connection
            self.client = mqtt.Client()
            #self.client.will_set("/device/+/unlock",self.client._client_id, 0, False)
            self.client.connect(Setting.Broker_ip)
            self.client.on_message = partial(on_message, data=self.data)
            #self.client.subscribe("/device/+", qos=0)
            self.client.loop_start()
        
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

def topic_in(a,b):
    t1=b.split("/")
    t2=a.split("/")  
    if t1[2]=="+" or  t1[2]==t2[2] :  #different topic
        if t1[3]=="+" or  t1[3]==t2[3] :
            if t1[4]=="+" or  t1[4]==t2[4] :
                return True
    return False  

#_/device/id1/type1/location1
#_/device/id2/type2/location2
        
        


'''
a="/device/+/temp/123"
b="/device/+/temp/+"   
x=ShadowBroker()

x.listenComplex("+","temp","+")
x.listenComplex("+","temp","123")
x.listenComplex("5","hue","123")
x.listenComplex("+","hue","+")
x.listenComplex("5","+","+")

print(x.getShadow("asd"))
print(x.topic_print())


  
x=ShadowBroker()
x.listenComplex("asd","asd")
x.listenLocation("asd")
time.sleep(10)
x.publish("/device/1/asd/asd","ciao")
time.sleep(10)
print(id(x),"  ",x.topic_print())
y=ShadowBroker()
print(id(y),"  ",y.topic_print())
'''