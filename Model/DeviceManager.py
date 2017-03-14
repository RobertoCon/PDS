'''
Created on 15 gen 2017

@author: Conny
from concurrent.futures import ThreadPoolExecutor
#ThreadPoolExecutor(max_workers=1)

'''

from pathlib import Path
from functools import partial
from Model import Setting
import paho.mqtt.client as mqtt
import yaml,json
from Device.Factory import Factory
from concurrent.futures import ThreadPoolExecutor

class DeviceManager(object):

    def __init__(self):
        self.devices={}
        self.links={}
        self.pool=ThreadPoolExecutor(max_workers=16)
        self.path = Path(Setting.path+"./Settings/").absolute()
        self.path=self.path.joinpath("DeviceRegistry.yaml")
        if self.path.is_file() == False :
            yaml.dump(self.devices,open(str(self.path),'w')) 
        else:
            self.devices=yaml.load(open(str(self.path),'r'))
            for dev in self.devices['node_templates']:
                device=Factory.decode(json.dumps(self.devices['node_templates'][dev]))
                self.links[dev]=type(device).make_active(device, self.pool)
        print("Device loaded")
                 
        def on_message_add(client, userdata, message, obj):
            serial_frame=str(message.payload.decode("utf-8"))
            yaml_frame=yaml.load(serial_frame)
            for dev in yaml_frame['node_templates']:
                device=Factory.decode(json.dumps(yaml_frame['node_templates'][dev]))
                if device!=None and device.id not in obj.devices['node_templates']: 
                    obj.links[dev]=type(device).make_active(device, self.pool) 
                    obj.devices['node_templates'][dev]=yaml_frame['node_templates'][dev] 
                
            obj.permanent()  
            obj.publish()
        
        def on_message_remove(client, userdata, message, obj):
            serial_frame=str(message.payload.decode("utf-8"))
            yaml_frame=yaml.load(serial_frame)
            for dev in yaml_frame['node_templates']:
                if dev in obj.devices['node_templates']:
                    obj.devices['node_templates'].pop(dev) 
                    
                    
                    obj.links[dev].terminate() 
                    #obj.links[dev].kill() 
                   
                    obj.links.pop(dev)
            obj.permanent()  
            obj.publish() 
            
        def on_message_read(client, userdata, message, obj):
            obj.publish()
            
                     
        self.client = mqtt.Client()
        self.client.will_set("/"+Setting.getNodeId()+"/model/device/status",yaml.dump('{node_templates:{}}'), 0, True)
        self.client.message_callback_add("/"+Setting.getNodeId()+"/model/device/add", partial(on_message_add, obj=self)) 
        self.client.message_callback_add("/"+Setting.getNodeId()+"/model/device/remove", partial(on_message_remove, obj=self))
        self.client.message_callback_add("/"+Setting.getNodeId()+"/model/device/read", partial(on_message_read, obj=self))
        self.client.connect(Setting.getBrokerIp())
        self.client.loop_start()        
        self.client.subscribe("/"+Setting.getNodeId()+"/model/device/add", qos=0)
        self.client.subscribe("/"+Setting.getNodeId()+"/model/device/remove", qos=0)
        self.client.subscribe("/"+Setting.getNodeId()+"/model/device/read", qos=0)
        self.publish()        
    
    def permanent(self):
        yaml.dump(self.devices,open(str(self.path),'w'))
        
    def publish(self):
        self.client.publish("/"+Setting.getNodeId()+"/model/device/status",yaml.dump(self.devices),qos=0,retain=True)