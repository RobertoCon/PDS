'''
Created on 26 ott 2016

@author: Conny
'''
from Model import Setting
import paho.mqtt.client as mqtt
import threading
            
            
    
class MqttClient(object):
    class __MqttClient(object):            
        def __init__(self):      
            self.locker=threading.RLock()
            self.client = mqtt.Client()
            self.client.connect(Setting.getBrokerIp())
            self.client.loop_start()
            self.start()
    
        def subscribe(self,topic,qos,callback):
            with self.locker:
                self.client.message_callback_add(topic, callback)
                self.client.subscribe(topic, qos)
        
        def unsubscribe(self,topic):
            with self.locker:
                self.client.unsubscribe(topic)
        
          
        def publish(self,topic,message,qos,retain):
            with self.locker:
                self.client.publish(topic,message,qos,retain)
            
    
    instance = None  
    def __init__(self):
        if not MqttClient.instance:
            MqttClient.instance = MqttClient.__MqttClient()
    def __getattr__(self, name):
        return getattr(self.instance, name)
    def __setattr__(self, name):
        return setattr(self.instance, name)