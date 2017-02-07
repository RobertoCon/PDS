'''
Created on 07 feb 2017

@author: Conny
'''
from pathlib import Path
from functools import partial
from Model import Setting
import paho.mqtt.client as mqtt
import yaml
from Dev.Factory import Factory

class DeviceManager(object):

    def __init__(self):
        self.devices={}
        self.links={}
        
        self.path = Path(Setting.path+"../Settings/").absolute()
        self.path=self.path.joinpath("DeviceRegistry.yaml")
        self.devices=yaml.load(open(str(self.path),'r'))
        for dev in self.devices['node_templates']:
            print(self.devices['node_templates'])
        
        print("Device loaded")
        self.devices['node_templates']['id1']="asdasdasd" 
        self.devices['node_templates']['id2']="qweqwe" 
        for dev in self.devices['node_templates']:
            print(self.devices['node_templates'][dev])
        
        print("Device loaded")
   
DeviceManager()