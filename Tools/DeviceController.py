'''
Created on 15 gen 2017

@author: Conny
'''

from Model import Setting
import paho.mqtt.client as mqtt
import time

yaml = """
node_templates:
    dev3:
        id: dev4
        type: my.Device.TempSensor
        location: bathroom
        device_type: TempSensor
        requirements:
          host: py_2"""
      
client = mqtt.Client()
client.connect(Setting.Broker_ip)
client.loop_start()        
client.publish("/"+Setting.node_id+"/model/device/add/",yaml, 0)  

time.sleep(5)