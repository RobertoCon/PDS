'''
Created on 16 gen 2017

@author: Conny
'''
from Dashboard.NodeTable import NodeTable
from Dashboard.DeviceTable import DeviceTable
from Dashboard.AppTable import AppTable
import cherrypy
import yaml,json
from pathlib import Path
import paho.mqtt.client as mqtt 
from functools import partial
from Model import Setting
import subprocess

class Dashboard(object):

    def __init__(self):
        super(Dashboard,self).__init__()
        self.nodes={'node_templates':{}}
        self.devices={'node_templates':{}}
        self.apps={'node_templates':{}}
        
        def on_message_node(client, userdata, message, obj):
            serial_frame=str(message.payload.decode("utf-8"))
            yaml_frame=yaml.load(serial_frame)
            for node in yaml_frame['node_templates']:  
                if node not in obj.nodes['node_templates']:
                    obj.nodes['node_templates'][node]=yaml_frame['node_templates'][node] 
                else:
                    pass
                
            
            
        def on_message_device(client, userdata, message, obj):
            serial_frame=str(message.payload.decode("utf-8"))
            yaml_frame=yaml.load(serial_frame)
            for dev in yaml_frame['node_templates']:  
                if dev not in obj.devices['node_templates']:
                    obj.devices['node_templates'][dev]=yaml_frame['node_templates'][dev] 
                else:
                    pass
                
        def on_message_app(client, userdata, message, obj):
            serial_frame=str(message.payload.decode("utf-8"))
            yaml_frame=yaml.load(serial_frame)
            for app in yaml_frame['node_templates']:  
                if app not in obj.apps['node_templates']:
                    obj.apps['node_templates'][app]=yaml_frame['node_templates'][app] 
                else:
                    pass
                
        self.client = mqtt.Client()
        self.client.message_callback_add("/+/model/node/status", partial(on_message_node, obj=self)) 
        self.client.message_callback_add("/+/model/device/status", partial(on_message_device, obj=self)) 
        self.client.message_callback_add("/+/model/apps/status", partial(on_message_app, obj=self)) 
        self.client.connect(Setting.getBrokerIp())
        self.client.loop_start()        
        self.client.subscribe("/+/model/node/status", qos=0)
        self.client.subscribe("/+/model/device/status", qos=0) 
        self.client.subscribe("/+/model/apps/status", qos=0)       
        
        
        
        self.structure="""<html>
        <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">
        </head>
        <body>
            <nav class="navbar navbar-inverse navbar-fixed-top">
              <div class="container">
                <div class="navbar-header">
                  <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
                    <span class="sr-only">Toggle navigation</span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                    <span class="icon-bar"></span>
                  </button>
                  <a class="navbar-brand" href="/">Project name</a>
                </div>
                <div id="navbar" class="collapse navbar-collapse">
                  <ul class="nav navbar-nav">
                    <li class="active"><a href="/">Home</a></li>
                    <li><a href="/node">Node</a></li>
                    <li><a href="/device">Device</a></li>
                    <li><a href="/app">Appse</a></li>
                    <li><a href="/about">About</a></li>
                    <li><a href="/contact">Contact</a></li>
                  </ul>
                </div><!--/.nav-collapse -->
              </div>
            </nav>
            <br><br><br>
            %s
        </body>
        </html>
        """
   

    @cherrypy.expose
    def index(self):
        
        return self.structure % ("index")
    
    #Node Managment
    @cherrypy.expose
    def node(self):
        return self.structure % (NodeTable.getHtml(self.nodes))
    
    @cherrypy.expose   
    def remove_node(self,remove_node_id):
        if remove_node_id in self.nodes['node_templates']:
            self.nodes['node_templates'].pop(remove_node_id)
            opt=subprocess.Popen("/opt/emqttd/bin/emqttd_ctl cluster remove emqttd@"+remove_node_id+"." , stdout=subprocess.PIPE, shell=True)
            opt.wait()
            #self.client.publish("/"+remove_node_id+"/model/node/remove", "remove_mex", 0, False)
        raise cherrypy.HTTPRedirect("/node")
    
    @cherrypy.expose   
    def add_node(self,add_node_id):
        #my_path = Path(Setting.path+"./Settings/").absolute()
        #my_path=my_path.joinpath("NodeRegistry.yaml")
        #my_node=yaml.load(open(str(my_path),'r')) 
        #new_client = mqtt.Client()
        #new_client.connect(add_node_id)
        #new_client.loop_start()        
        #new_client.publish("/"+add_node_id+"/model/node/add", yaml.dump(my_node), 0, False)
        #new_client.disconnect()
        opt=subprocess.Popen("/opt/emqttd/bin/emqttd_ctl cluster join emqttd@"+add_node_id+"." , stdout=subprocess.PIPE, shell=True)
        opt.wait()
        raise cherrypy.HTTPRedirect("/node")
    
    
    #Device Managment
    @cherrypy.expose
    def device(self):
        return self.structure % (DeviceTable.getHtml(self.devices))
    
    @cherrypy.expose   
    def add_device(self,add_device_model):
        devs=yaml.load(add_device_model)
        for dev in devs['node_templates']:
            if dev not in self.devices['node_templates']:
                self.client.publish("/"+devs['node_templates'][dev]['requirements']['host']+"/model/device/add", add_device_model, 0, False)
        raise cherrypy.HTTPRedirect("/device")
    
    
    @cherrypy.expose   
    def remove_device(self,remove_device_model):
        devs=yaml.load(remove_device_model)
        for dev in devs['node_templates']:
            if dev in self.devices['node_templates']:
                self.devices['node_templates'].pop(dev)
                self.client.publish("/"+devs['node_templates'][dev]['requirements']['host']+"/model/device/remove", yaml.dump(devs), 0, False) 
        raise cherrypy.HTTPRedirect("/device")
    
    
    
    
    
    
    #App Managment
    @cherrypy.expose
    def app(self):
        return self.structure % (AppTable.getHtml(self.apps))
    
    @cherrypy.expose   
    def add_app(self,add_app_model):
        apps_model=yaml.load(add_app_model)
        for app in apps_model['node_templates']:
            if app not in self.apps['node_templates']:
                self.client.publish("/"+apps_model['node_templates'][app]['requirements']['host']['node']+"/model/apps/add", add_app_model, 0, False)
        raise cherrypy.HTTPRedirect("/app")
    
    
    @cherrypy.expose   
    def remove_app(self,remove_app_model):
        apps_model=yaml.load(remove_app_model)
        for app in apps_model['node_templates']:
            if app in self.apps['node_templates']:
                self.apps['node_templates'].pop(app)
                self.client.publish("/"+apps_model['node_templates'][app]['requirements']['host']['node']+"/model/apps/remove", remove_app_model, 0, False) 
        raise cherrypy.HTTPRedirect("/app")
    
    @cherrypy.expose   
    def start_app(self,start_app_model):
        apps_model=yaml.load(start_app_model)
        for app in apps_model['node_templates']:
            if app in self.apps['node_templates']:
                self.client.publish("/"+apps_model['node_templates'][app]['requirements']['host']['node']+"/model/apps/start", start_app_model, 0, False) 
        raise cherrypy.HTTPRedirect("/app")
    
    @cherrypy.expose   
    def stop_app(self,stop_app_model):
        raise cherrypy.HTTPRedirect("/app")
    
    @cherrypy.expose   
    def update_app(self,stop_app_model):
        raise cherrypy.HTTPRedirect("/app")
    
    
    
    @cherrypy.expose
    def about(self):
        return self.structure % ("About")
    @cherrypy.expose
    def contact(self):
        return self.structure % ("Contact")