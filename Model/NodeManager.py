'''
Created on 15 gen 2017

@author: Conny
'''

from pathlib import Path
from functools import partial
from Model import Setting
import paho.mqtt.client as mqtt
import yaml
import subprocess

class NodeManager(object):

    def __init__(self):
        self.nodes={}
        self.path = Path(Setting.path+"./Settings/").absolute()
        self.path=self.path.joinpath("NodeRegistry.yaml")
        if self.path.is_file() == False :
            yaml.dump(self.nodes,open(str(self.path),'w')) 
        else:
            self.nodes=yaml.load(open(str(self.path),'r')) 
        print("Nodes loaded")
                 
        def on_message_add(client, userdata, message, obj):
            serial_frame=str(message.payload.decode("utf-8"))
            yaml_frame=yaml.load(serial_frame)
            for node in yaml_frame['node_templates']:  
                if node not in obj.nodes['node_templates']: 
                    #link 2 cluster
                    subprocess.Popen("/opt/emqttd/bin/emqttd_ctl cluster join "+node['attributes']['public_address'] , stdout=subprocess.PIPE, shell=True)
                    obj.nodes['node_templates'][node]=yaml_frame['node_templates'][node] 
            obj.permanent()  
            obj.publish()
        
        def on_message_remove(client, userdata, message, obj):
            serial_frame=str(message.payload.decode("utf-8"))
            yaml_frame=yaml.load(serial_frame)
            for node in yaml_frame['node_templates']:  
                if node in obj.nodes['node_templates']: 
                    #remove link 2 cluster
                    subprocess.Popen("/opt/emqttd/bin/emqttd_ctl cluster leave", stdout=subprocess.PIPE, shell=True)
                    obj.nodes['node_templates'].pop(node)
            obj.permanent()  
            obj.publish()
            
        def on_message_read(client, userdata, message, obj):
            obj.publish()
            
                     
        self.client = mqtt.Client()
        self.client.message_callback_add("/"+Setting.node_id+"/model/node/add", partial(on_message_add, obj=self)) 
        self.client.message_callback_add("/"+Setting.node_id+"/model/node/remove", partial(on_message_remove, obj=self))
        self.client.message_callback_add("/"+Setting.node_id+"/model/node/read", partial(on_message_read, obj=self))
        self.client.connect(Setting.Broker_ip)
        self.client.loop_start()        
        self.client.subscribe("/"+Setting.node_id+"/model/node/add", qos=0)
        self.client.subscribe("/"+Setting.node_id+"/model/node/remove", qos=0)
        self.client.subscribe("/"+Setting.node_id+"/model/node/read", qos=0)        
        self.publish()
        
    def permanent(self):
        yaml.dump(self.nodes,open(str(self.path),'w'))
        
    def publish(self):
        self.client.publish("/"+Setting.node_id+"/model/node/status",yaml.dump(self.nodes),qos=0,retain=True)