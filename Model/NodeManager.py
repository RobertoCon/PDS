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
            exit(-1)
        else:
            self.nodes=yaml.load(open(str(self.path),'r')) 
            for node in self.nodes['node_templates']:
                self.nodes['node_templates'][node]['id']=Setting.getHostName()
                self.nodes['node_templates'][node]['attributes']['public_address']=Setting.getIp()
                self.nodes['node_templates'][node]['attributes']['broker_address']=Setting.getIp()
                if node == "node":
                    self.nodes['node_templates'][Setting.getHostName()]=self.nodes['node_templates']['node']
                    self.nodes['node_templates'].pop('node') 
        
        self.permanent()
        print("Node loaded")  
           
        def on_message_add(client, userdata, message, obj):
            print("Request to join cluster")
            serial_frame=str(message.payload.decode("utf-8"))
            yaml_frame=yaml.load(serial_frame)
            for node in yaml_frame['node_templates']:  
                #if node not in obj.nodes['node_templates']: 
                    #link 2 cluster
                    #obj.client.publish("/"+Setting.getNodeId()+"/model/node/status",None,qos=0,retain=True)
                    opt=subprocess.Popen("/opt/emqttd/bin/emqttd_ctl cluster join emqttd@"+yaml_frame['node_templates'][node]['id']+"." , stdout=subprocess.PIPE, shell=True)
                    if opt.wait() :
                        obj.publish()
        
        def on_message_remove(client, userdata, message, obj):
            print("Request to leave cluster")
            #serial_frame=str(message.payload.decode("utf-8"))
            #yaml_frame=yaml.load(serial_frame)
            #obj.client.publish("/"+Setting.getNodeId()+"/model/node/status",None,qos=0,retain=True)
            opt=subprocess.Popen("/opt/emqttd/bin/emqttd_ctl cluster leave", stdout=subprocess.PIPE, shell=True)
            if opt.wait() :
                obj.publish()
            
            
        def on_message_read(client, userdata, message, obj):
            obj.publish()      
                     
        self.client = mqtt.Client()
        self.client.will_set("/"+Setting.getNodeId()+"/model/node/status",None, 0, True)
        self.client.message_callback_add("/"+Setting.getNodeId()+"/model/node/add", partial(on_message_add, obj=self)) 
        self.client.message_callback_add("/"+Setting.getNodeId()+"/model/node/remove", partial(on_message_remove, obj=self))
        self.client.message_callback_add("/"+Setting.getNodeId()+"/model/node/read", partial(on_message_read, obj=self))
        self.client.connect(Setting.getBrokerIp())
        self.client.loop_start()        
        self.client.subscribe("/"+Setting.getNodeId()+"/model/node/add", qos=0)
        self.client.subscribe("/"+Setting.getNodeId()+"/model/node/remove", qos=0)
        self.client.subscribe("/"+Setting.getNodeId()+"/model/node/read", qos=0)        
        self.publish()
        
    def permanent(self):
        yaml.dump(self.nodes,open(str(self.path),'w'))
        
    def publish(self):
        self.client.publish("/"+Setting.getNodeId()+"/model/node/status",yaml.dump(self.nodes),qos=0,retain=True)