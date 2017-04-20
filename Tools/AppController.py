'''
@author: Conny
'''
import paho.mqtt.client as mqtt
import time,yaml
host='raspy3-A'
client = mqtt.Client()
client.connect(host)
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
                    node: '''+host+'''
                    cpu_quota: 100000
                    relationship: HostedOn
                    bootstrap: yes
                    state: online'''

client.publish("/"+host+"/model/apps/add",msg, 0, False)
print("Sending .....")
time.sleep(3)
print("Done")

