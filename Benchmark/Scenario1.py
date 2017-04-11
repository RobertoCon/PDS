'''
Created on 11 apr 2017

@author: Conny
'''
'''
Created on 21 mar 2017

@author: Conny
'''
import time,yaml
from ApplicationLayer.PDS import RASPBERRYPI
import paho.mqtt.client as mqtt
from Model import Setting

app=yaml.load('''node_templates:                                        
    app1:
            instance: stress1
            type: tosca.nodes.Container.Application.Docker
            properties:
                ports:
                    in_port:
                        protocol: tcp
                        target: 50000
            artifacts:
                image: 
                   file: stress-test
                   repository: docker_hub
                   description: busy-box
            requirements:
                host:
                    node:  raspy3-A
                    cpu_quota: 30000
                    relationship: HostedOn
                    bootstrap: yes
                    state: online''')
                    
client = mqtt.Client()
client.connect(Setting.getBrokerIp())
client.loop_start()        
while True:   
    
    py=RASPBERRYPI().map(lambda x : x.hostname)
    
    print("Hostname : ",py)
    for host in py:
        client.publish("/"+host+"/model/apps/add",yaml.dump(app),qos=0,False)
        time.sleep(30)
        client.publish("/"+host+"/model/apps/stop",yaml.dump(app),qos=0,False)
    
     
        
        #self.client.message_callback_add("/"+Setting.getNodeId()+"/model/apps/add", partial(on_message_add, obj=self)) 
        #self.client.message_callback_add("/"+Setting.getNodeId()+"/model/apps/start", partial(on_message_start, obj=self)) 
        #self.client.message_callback_add("/"+Setting.getNodeId()+"/model/apps/stop", partial(on_message_stop, obj=self))

#client.publish("/"+Setting.getNodeId()+"/model/apps/add",yaml.dump(app),qos=0,False)
    
