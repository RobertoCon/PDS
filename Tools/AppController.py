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
client.connect('raspy3-A')
client.loop_start()
client.on_message = on_message

msg='''node_templates:                                        
    scen1:
            instance: scen1
            type: tosca.nodes.Container.Application.Docker
            properties:
                ports:
                    in_port:
                        protocol: tcp
                        target: 50000
            artifacts:
                image: 
                   file: scenario1
                   repository: docker_hub
                   description: busy-box
            requirements:
                host:
                    node: raspy3-A
                    cpu_quota: 30000
                    relationship: HostedOn
                    bootstrap: yes
                    state: online'''

client.publish("/raspy3-A/model/apps/add", msg, 0, False)
print("Sending .....")
time.sleep(3)
print("Done")

