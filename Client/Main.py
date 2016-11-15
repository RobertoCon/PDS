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
client.will_set("/device/+/unlock",None, 0, True)
client.connect(Setting.Broker_ip)
client.loop_start()
time.sleep(5)


