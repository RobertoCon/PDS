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
#msg={'cmd':'run','appl':'{"app_name":"app2","cpu_quota":"20000","image_name":"test-python"}'}
#msg={'cmd':'regist','appl':'{"app_name":"app1","cpu_quota":"30000","image_name":"test-python"}'}

msg={'cmd':'stop','appl':'{"app_name" : "app1","type":"busy-box","boot":"yes","image_name" : "test-python","cpu_quota":"10000","scalingV":"True""scalingH":"True""Migrate": "False""SharedM": "App1Tag" }'}
client.publish("/application/registry/id1",json.dumps(msg),0,retain=False)
print("Sending .....")
time.sleep(3)
print("Done")

'''

{'app_name' : 'Application1A','type':'','image_name' : 'Application1','cpu_quota':'10000','scalingV':'True''scalingH':'True''Migrate': 'False''SharedM': 'App1Tag' }

'''