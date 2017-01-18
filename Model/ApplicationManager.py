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

class ApplicationManager(object):

    def __init__(self):
        self.apps={}
        self.path = Path(Setting.path+"../Settings/").absolute()
        self.path=self.path.joinpath("ApplicationRegistry.yaml")
        if self.path.is_file() == False :
            yaml.dump(self.apps,open(str(self.path),'w')) 
        else:
            self.apps=yaml.load(open(str(self.path),'r'))
            for app in self.apps['node_templates']:
                    if self.apps['node_templates'][app]['requirements']['host']['bootstrap']=='yes':
                        print(self.apps['node_templates'][app])
                        #self.docker_start(self.apps['node_templates'][app])
        print("Applications loaded")
        
        
        def on_message_add(client, userdata, message, obj):
            serial_frame=str(message.payload.decode("utf-8"))
            yaml_frame=yaml.load(serial_frame)
            for app in yaml_frame['node_templates']:
                if app not in obj.apps['node_templates']: 
                    obj.apps['node_templates'][app]=yaml_frame['node_templates'][app] 
                    obj.docker_run(yaml_frame['node_templates'][app])
            obj.permanent()  
            obj.publish()
            
        def on_message_remove(client, userdata, message, obj):
            serial_frame=str(message.payload.decode("utf-8"))
            yaml_frame=yaml.load(serial_frame)
            for app in yaml_frame['node_templates']:
                if app in obj.apps['node_templates']:
                    obj.apps['node_templates'].pop(app) 
                    obj.docker_remove(yaml_frame['node_templates'][app])
            obj.permanent()  
            obj.publish()
            
        def on_message_start(client, userdata, message, obj):
            serial_frame=str(message.payload.decode("utf-8"))
            yaml_frame=yaml.load(serial_frame)
            for app in yaml_frame['node_templates']:
                if app in obj.apps['node_templates']: 
                    obj.apps['node_templates'][app]=yaml_frame['node_templates'][app] 
                    obj.docker_start(yaml_frame['node_templates'][app])
            obj.permanent()  
            obj.publish()
            
        def on_message_stop(client, userdata, message, obj):
            serial_frame=str(message.payload.decode("utf-8"))
            yaml_frame=yaml.load(serial_frame)
            for app in yaml_frame['node_templates']:
                if app in obj.apps['node_templates']:
                    obj.apps['node_templates'][app]=yaml_frame['node_templates'][app] 
                    obj.docker_stop(yaml_frame['node_templates'][app])
            obj.permanent()  
            obj.publish()
            
        def on_message_update(client, userdata, message, obj):
            serial_frame=str(message.payload.decode("utf-8"))
            yaml_frame=yaml.load(serial_frame)
            for app in yaml_frame['node_templates']:
                if app in obj.apps['node_templates']:
                    obj.apps['node_templates'][app]=yaml_frame['node_templates'][app] 
                    obj.docker_update(yaml_frame['node_templates'][app])
            obj.permanent()  
            obj.publish()
            
        def on_message_read(client, userdata, message, obj):
            obj.publish()
            
        self.client = mqtt.Client()
        self.client.message_callback_add("/"+Setting.node_id+"/model/apps/add", partial(on_message_add, obj=self)) 
        self.client.message_callback_add("/"+Setting.node_id+"/model/apps/remove", partial(on_message_remove, obj=self))
        self.client.message_callback_add("/"+Setting.node_id+"/model/apps/read", partial(on_message_read, obj=self))
        self.client.message_callback_add("/"+Setting.node_id+"/model/apps/start", partial(on_message_start, obj=self)) 
        self.client.message_callback_add("/"+Setting.node_id+"/model/apps/stop", partial(on_message_stop, obj=self))
        self.client.message_callback_add("/"+Setting.node_id+"/model/apps/update", partial(on_message_update, obj=self))
        self.client.connect(Setting.Broker_ip)
        self.client.loop_start()        
        self.client.subscribe("/"+Setting.node_id+"/model/apps/add", qos=0)
        self.client.subscribe("/"+Setting.node_id+"/model/apps/remove", qos=0)
        self.client.subscribe("/"+Setting.node_id+"/model/apps/read", qos=0) 
        self.client.subscribe("/"+Setting.node_id+"/model/apps/start", qos=0)
        self.client.subscribe("/"+Setting.node_id+"/model/apps/stop", qos=0)
        self.client.subscribe("/"+Setting.node_id+"/model/apps/update", qos=0) 
    
    def docker_start(self,app):
        #print("Docker CMD : docker start "+app_json['app_name'] )
        subprocess.Popen("docker start "+app['instance'] , stdout=subprocess.PIPE, shell=True)
    
    #"docker run -it --rm --cpu-quota=30000  --name my-running-app test-python"      
    def docker_run(self,app):
        #print("Docker CMD : docker run --cpu-quota="+app_json['cpu_quota']+" --name "+app_json['app_name']+" "+app_json['image_name'])
        subprocess.Popen("docker run --cpu-quota="+app['requirements']['host']['cpu_quota']+" --name "+app['instance']+" "+app['artifacts']['image']['file'], stdout=subprocess.PIPE, shell=True)
      
    def docker_stop(self,app):
        #print("Docker CMD : docker stop "+app_json['app_name'] )
        subprocess.Popen("docker stop "+app['instance'] , stdout=subprocess.PIPE, shell=True)
        
    def docker_remove(self,app):
        #print("Docker CMD : docker rm "+app_json['app_name'] )
        subprocess.Popen("docker rm "+app['instance'] , stdout=subprocess.PIPE, shell=True)
    
    def docker_update(self,app):
        #print("Docker CMD : docker update --cpu-quota="+app_json['cpu_quota']+" --name "+app_json['app_name'])
        subprocess.Popen("docker update --cpu-quota="+app['requirements']['host']['cpu_quota']+" "+app['instance'], stdout=subprocess.PIPE, shell=True)

    def permanent(self):
        yaml.dump(self.apps,open(str(self.path),'w')) 
        
    def publish(self):
        self.client.publish("/"+Setting.node_id+"/model/apps/status",yaml.dump(self.apps),qos=0,retain=True)