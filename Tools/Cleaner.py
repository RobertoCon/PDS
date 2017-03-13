'''
Created on 01 nov 2016

@author: Conny
'''
import paho.mqtt.client as mqtt
import time
from Model import Setting

def on_message(client, userdata, message):
        print("Received message '" + str(message.payload) + "' on topic '"+ message.topic + "' with QoS " + str(message.qos))
        client.publish(message.topic,None,0,retain=True)
        
client = mqtt.Client()
#client.connect(Setting.getBrokerIp())
client.connect("192.168.1.5")
client.loop_start()
client.on_message = on_message
client.subscribe("/#", qos=0)
print("Start cleaning .....")
time.sleep(20)
print("Stop cleaning")
