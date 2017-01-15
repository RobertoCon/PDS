'''
Created on 15 gen 2017

@author: Conny
'''

from pathlib import Path
from functools import partial
from Model import Setting
import paho.mqtt.client as mqtt
import yaml
from Dev.Factory import Factory

class ModelManager(object):

    def __init__(self):
        self.devices={}
        self.nodes={}
        self.apps={}
        self.apps={}
        self.model={}
        
        self.path = Path(Setting.path+"../Settings/").absolute()
        #self.path.mkdir(parents=True, exist_ok=True)
        self.path=self.path.joinpath("DeviceRegistry.yaml")
        
        if self.path.is_file() == False :
            yaml.dump(self.devices,open(str(self.path),'w')) 
        else:
            #read it
            self.devices=yaml.load(open(str(self.path),'r'))
            for dev in self.devices['node_templates']:
                device=Factory.decode_yaml(yaml.dump(self.devices['node_templates'][dev]))
                if device!=None:
                    type(device).make_active(device) 
                    #self.devices['node_templates'][dev]['object']=device
        print(yaml.dump(self.devices))
        print("-----------------")
                 
        def on_message_add(client, userdata, message, obj):
            serial_frame=str(message.payload.decode("utf-8"))
            yaml_frame=yaml.load(serial_frame)
            for dev in yaml_frame['node_templates']:
                device=Factory.decode_yaml(yaml.dump(yaml_frame['node_templates'][dev]))
                if device!=None:
                    type(device).make_active(device) 
                    obj.devices['node_templates'][dev]=yaml_frame['node_templates'][dev]
            obj.permanent()  
        
        def on_message_remove(client, userdata, message, obj):
            serial_frame=str(message.payload.decode("utf-8"))
            yaml_frame=yaml.load(serial_frame)
            device=Factory.decode_yaml(yaml.dump(yaml_frame))
            if device!=None:
                type(device).make_active(device) 
                obj.devices.append(yaml_frame)
            obj.permanent()     
                     
        self.client = mqtt.Client()
        self.client.message_callback_add("/"+Setting.node_id+"/model/device/add/", partial(on_message_add, obj=self)) 
        self.client.message_callback_add("/"+Setting.node_id+"/model/device/remove/", partial(on_message_remove, obj=self))
        self.client.connect(Setting.Broker_ip)
        self.client.loop_start()        
        self.client.subscribe("/"+Setting.node_id+"/model/device/add/", qos=0)
        self.client.subscribe("/"+Setting.node_id+"/model/device/remove/", qos=0)        
    
    def permanent(self):
        yaml.dump(self.devices,open(str(self.path),'w'))
        
ModelManager()