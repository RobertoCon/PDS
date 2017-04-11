'''
Created on 11 apr 2017

@author: Conny
'''

import sys
sys.path.insert(0, "/pds")
import yaml,time
from ApplicationLayer.PDS import RASPBERRYPI
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

host=subprocess.getoutput("hostname -i")
app['node_templates']['scen1']['requirements']['host']['node']=host
client = mqtt.Client()
client.connect(host)
client.loop_start()   
shared=SharedMemory()
shared_key='scen1'
visited=shared.read(shared_key)
if visited==None:
    visited=[]
    
def threaded_function(arg):
    while True:
        pass

thread = Thread(target = threaded_function, args = (10, ))
thread.start()
while True:
    py=RASPBERRYPI().map(lambda x : x.hostname)
    time.sleep(60)
    next_host=random.choice(py)
    client.publish("/logger",("App su : ",host," si trasf su: ",next_host),qos=0)
    if host!=next:
        next_model=app
        next_model['node_templates']['scen1']['requirements']['host']['node']=next_host
        visited=shared.read(shared_key)
        if visited==None:
            visited=[]
        if host not in visited:
            visited.append(host) 
            shared.write(shared_key, visited)
            client.publish("/"+next_host+"/model/apps/add",yaml.dump(next_model),qos=0)
            client.publish("/"+host+"/model/apps/stop",yaml.dump(app),qos=0)
        else:
            shared.write(shared_key, visited)
            client.publish("/"+next_host+"/model/apps/start",yaml.dump(next_model),qos=0)
            client.publish("/"+host+"/model/apps/stop",yaml.dump(app),qos=0)