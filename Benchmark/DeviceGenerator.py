'''
Created on 11 mar 2017

@author: Conny
'''
from Model import Setting
import paho.mqtt.client as mqtt
import random
import string
import yaml

class DeviceGenerator(object):

    def __init__(self,template=None):
        if template!=None:
            self.template=yaml.load(template)
        else:
            self.template=yaml.load('''node_templates:
                                          dev:
                                            type_dev: TempSensor
                                            id_dev: dev
                                            location_dev: bathroom
                                            requirements: {host: raspy3-A}
                                            type: my.Device.TempSensor
                                            temperature: 0
                                            unit: celsius''')
        self.client = mqtt.Client()
        self.client.connect(Setting.getBrokerIp())
        self.client.loop_start()       
      
    def make(self,number,location=['not_available'],host=['']):
        for i in range(number):
            model={'node_templates':{}}
            id_dev=self.id_generator()
            model['node_templates'][id_dev]=self.template['node_templates']['dev']
            model['node_templates'][id_dev]['id_dev']=id_dev
            model['node_templates'][id_dev]['location_dev']=random.choice(location)
            model['node_templates'][id_dev]['requirements']['host']=random.choice(host)
            self.id_generator()
            self.client.publish("/"+model['node_templates'][id_dev]['requirements']['host']+"/model/device/add", yaml.dump(model), 0, False)
    
    def id_generator(self,size=10, chars=string.ascii_uppercase + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))