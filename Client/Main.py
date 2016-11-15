'''
Created on 01 nov 2016

@author: Conny
'''
from ApplicationLayer.PDS import PDS, HUE ,TEMP
from ApplicationLayer.ShadowBroker import ShadowBroker
import paho.mqtt.client as mqtt
import time
from Model import Setting


client = mqtt.Client()
client.connect(Setting.Broker_ip)
client.loop_start()

client.publish("/device/hue1/lock",client._client_id, qos=0)
time.sleep(40)
client.publish("/device/hue1/unlock",client._client_id, qos=0)
time.sleep(5)


