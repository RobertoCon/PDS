'''
@author: Conny
'''
import paho.mqtt.client as mqtt
import time
from Model import Setting
import json

def on_message(client, userdata, message):
        print("Received message '" + str(message.payload) + "' on topic '"+ message.topic + "' with QoS " + str(message.qos))
        
        
client = mqtt.Client()
client.connect(Setting.Broker_ip)
client.loop_start()
client.on_message = on_message
msg={'cmd':'run','appl':'{"app_name":"app1","cpu_quota":"10000","image_name":"test-python"}'}
client.publish("/application/registry/id1",json.dumps(msg),0,retain=False)
print("Sending .....")
time.sleep(3)
print("Done")

'''

{'cmd':'','appl':"'{'app_name':'app1','cpu_quota':'10000','image_name':'test-python'}'"}

'''