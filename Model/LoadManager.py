'''
Created on 15 gen 2017

@author: Conny
'''

from pathlib import Path
from functools import partial
from Model import Setting
import paho.mqtt.client as mqtt
import yaml
import  subprocess

class LoadManager(object):

    def __init__(self):
        self.balancers={}
        self.path = Path(Setting.path+"./Settings/").absolute()
        self.path=self.path.joinpath("LoadRegistry.yaml")
        if self.path.is_file() == False :
            yaml.dump(self.balancers,open(str(self.path),'w')) 
        else:
            self.balancers=yaml.load(open(str(self.path),'r'))
            self.update_balancer()
        print("Balancer loaded")
                 
        def on_message_add(client, userdata, message, obj):
            serial_frame=str(message.payload.decode("utf-8"))
            yaml_frame=yaml.load(serial_frame)
            for app in yaml_frame['node_templates']:
                if  app not in obj.balancers['node_templates']: 
                    obj.balancers['node_templates'][app]=yaml_frame['node_templates'][app] 
            obj.permanent()  
            obj.publish()
            obj.update_balancer()
        
        def on_message_remove(client, userdata, message, obj):
            serial_frame=str(message.payload.decode("utf-8"))
            yaml_frame=yaml.load(serial_frame)
            for app in yaml_frame['node_templates']:
                if  app in obj.balancers['node_templates']: 
                    obj.balancers['node_templates'].pop(app) 
            obj.permanent()  
            obj.publish()
            obj.update_balancer()
            
        def on_message_read(client, userdata, message, obj):
            obj.publish()
            
                     
        self.client = mqtt.Client()
        self.client.will_set("/"+Setting.getNodeId()+"/model/balancer/status",'''node_templates: {}\n''', 0, True)
        self.client.message_callback_add("/"+Setting.getNodeId()+"/model/balancer/add", partial(on_message_add, obj=self)) 
        self.client.message_callback_add("/"+Setting.getNodeId()+"/model/balancer/remove", partial(on_message_remove, obj=self))
        self.client.message_callback_add("/"+Setting.getNodeId()+"/model/balancer/read", partial(on_message_read, obj=self))
        self.client.connect(Setting.getBrokerIp())
        self.client.loop_start()        
        self.client.subscribe("/"+Setting.getNodeId()+"/model/balancer/add", qos=0)
        self.client.subscribe("/"+Setting.getNodeId()+"/model/balancer/remove", qos=0)
        self.client.subscribe("/"+Setting.getNodeId()+"/model/balancer/read", qos=0) 
        self.publish()       
    
    def permanent(self):
        yaml.dump(self.balancers,open(str(self.path),'w'))
        
    def publish(self):
        self.client.publish("/"+Setting.getNodeId()+"/model/balancer/status",yaml.dump(self.balancers),qos=0,retain=True)
        
    def update_balancer(self):
        default="""worker_processes  1;
events {
    worker_connections  1024;
}\n"""
        for app in self.balancers['node_templates']:
            server="\tserver {\n\t\tlisten\t"+str(self.balancers['node_templates'][app]['properties']['ports']['in_port']['target'])\
            +";\n\t\tproxy_pass "+self.balancers['node_templates'][app]['name']+";\n\t}"
                    
            stream="\tupstream "+self.balancers['node_templates'][app]['name']+"{\n"
            for link in self.balancers['node_templates'][app]['requirements']['application']:
                ip=self.balancers['node_templates'][app]['requirements']['application'][link]['ip_address']
                port=str(self.balancers['node_templates'][app]['requirements']['application'][link]['properties']['ports']['in_port']['target'])
                stream=stream+"\t\tserver "+ip+":"+port+";\n"
            stream=stream+"\t}"
            settings=default+"\n"+"stream {\n"+server+"\n"+stream+"\n}"
            path = Path("/usr/local/nginx/nginx.conf")
            if path.is_file() == True :
                f = open(str(path), 'w')
                f.write(settings)
                subprocess.Popen("/usr/local/nginx/nginx -s reload", stdout=subprocess.PIPE, shell=True)