'''
@author: Conny
'''
import paho.mqtt.client as mqtt
import time,yaml
  
client = mqtt.Client()
client.connect('raspy0-C')
client.loop_start()

msg='''node_templates:                                        
    scen1:
            instance: scen3
            type: tosca.nodes.Container.Application.Docker
            properties:
                ports:
                    in_port:
                        protocol: tcp
                        target: 50000
            artifacts:
                image: 
                   file: scenario3
                   repository: docker_hub
                   description: busy-box
            requirements:
                host:
                    node: raspy0-C
                    cpu_quota: 30000
                    relationship: HostedOn
                    bootstrap: yes
                    state: online'''

client.publish("/raspy0-C/model/apps/add",msg, 0, False)
print("Sending .....")
time.sleep(3)
print("Done")

