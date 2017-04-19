'''
Created on 11 apr 2017

@author: Conny
'''

import sys
sys.path.insert(0, "/pds/DevicePlugin")
sys.path.insert(0, "/pds/FunctionalLayer")
sys.path.insert(0, "/pds/")
import yaml,time,copy
from FunctionalLayer.RASPBERRYPI import RASPBERRYPI
import paho.mqtt.client as mqtt
import  subprocess
import random
from ApplicationManager.SharedMemory import SharedMemory
from threading import Thread

app=yaml.load('''node_templates:                                        
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
                    state: online''')

host=subprocess.getoutput("hostname")
app['node_templates']['scen1']['requirements']['host']['node']=host
client = mqtt.Client()
client.connect(host)
client.loop_start()   
client.publish("/log","import successo",qos=0)
shared=SharedMemory()
shared_key='scen1'
visited=shared.read(shared_key)
client.publish("/log","shared = "+yaml.dump(visited),qos=0)
if visited==None:
    visited=[] 

def threaded_function(arg):
    while True:
        pass

thread = Thread(target = threaded_function, args = (10, ))
thread.start()

client.publish("/log","thread creato con successo",qos=0)
while True:
    py=RASPBERRYPI().map(lambda x : x.hostname)
    client.publish("/log","py : "+yaml.dump(py),qos=0)
    time.sleep(30)
    next_host=random.choice(py) 
    client.publish("/log","Next host : "+next_host,qos=0)
'''
    if host!=next_host:
        next_model=copy.copy(app)
        next_model['node_templates']['scen1']['requirements']['host']['node']=next_host
        if host not in visited:
            visited.append(host) 
            shared.write(shared_key, visited)
            client.publish("/"+next_host+"/model/apps/add",yaml.dump(next_model),qos=0)
            client.publish("/"+host+"/model/apps/stop",yaml.dump(app),qos=0)
        else:
            shared.write(shared_key, visited)
            client.publish("/"+next_host+"/model/apps/start",yaml.dump(next_model),qos=0)
            client.publish("/"+host+"/model/apps/stop",yaml.dump(app),qos=0)
'''