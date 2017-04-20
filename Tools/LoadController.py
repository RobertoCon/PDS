'''
Created on 19 apr 2017

@author: Conny
'''
import paho.mqtt.client as mqtt
import time,yaml
  
client = mqtt.Client()
client.connect('raspy3-A')
client.loop_start()

msg='''node_templates:   
        load1:
                name: id_1 
                type: tosca.nodes.LoadBalancer   
                host: raspy3-A      
                properties: 
                    algorithm: RR 
                    ports:
                        in_port:
                            protocol: tcp
                            target: 8282
                capabilities:
                    clients: 
                        ip_address: raspy3-A
                requirements:
                    application:
                        app1:
                            ip_address: raspy3-A 
                            properties:
                                ports:
                                    in_port:
                                        target: 9000
                        app2:
                            ip_address: raspy0-C 
                            properties:
                                ports:
                                    in_port:
                                        target: 9000
                        app3:
                            ip_address: raspy0-B 
                            properties:
                                ports:
                                    in_port:
                                        target: 9000'''

client.publish("/raspy3-A/model/balancer/add",msg, 0, False)
print("Sending .....")
time.sleep(3)
print("Done")
