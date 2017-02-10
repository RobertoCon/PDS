'''
Created on 16 gen 2017

@author: Conny
'''
from Dashboard.NodeTable import NodeTable
import cherrypy
import yaml
from pathlib import Path
import paho.mqtt.client as mqtt 
from functools import partial
from Model import Setting

class Dashboard(object):

    def __init__(self):
        super(Dashboard,self).__init__()
        self.nodes={'node_templates':{}}
        def on_message(client, userdata, message, obj):
            serial_frame=str(message.payload.decode("utf-8"))
            yaml_frame=yaml.load(serial_frame)
            for node in yaml_frame['node_templates']:  
                if node not in obj.nodes['node_templates']:
                    obj.nodes['node_templates'][node]=yaml_frame['node_templates'][node] 
                else:
                    pass
         
        self.client = mqtt.Client()
        self.client.message_callback_add("/+/model/node/status", partial(on_message, obj=self)) 
        self.client.connect(Setting.getBrokerIp())
        self.client.loop_start()        
        self.client.subscribe("/+/model/node/status", qos=0)        
    

    @cherrypy.expose
    def index(self):
        return """
        <html><head>
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
                  <a class="navbar-brand" href="#">Project name</a>
                </div>
                <div id="navbar" class="collapse navbar-collapse">
                  <ul class="nav navbar-nav">
                    <li class="active"><a href="#">Home</a></li>
                    <li><a href="#about">About</a></li>
                    <li><a href="#contact">Contact</a></li>
                  </ul>
                </div><!--/.nav-collapse -->
              </div>
            </nav>
            <br><br><br><br>
            """+NodeTable.getHtml(self.nodes)+"""  
            <form action="add_node" method="post" >
                   <span class="label label-default"> Hostname:</span><input type="text" name="add_node_id">
                   <button type="submit" class="btn btn-default btn-lg"><span class="glyphicon glyphicon-plus" aria-hidden="true"></span></button>
            </form> 
            </div><!-- /.container -->
            <br><br><br>
            
        </body>
        </html>
        """
    @cherrypy.expose   
    def remove_node(self,remove_node_id):
        self.client.publish("/"+remove_node_id+"/model/node/remove", "remove_mex", 0, False)
        raise cherrypy.HTTPRedirect("/")
    
    @cherrypy.expose   
    def add_node(self,add_node_id):
        my_path = Path(Setting.path+"./Settings/").absolute()
        my_path=my_path.joinpath("NodeRegistry.yaml")
        my_node=yaml.load(open(str(my_path),'r')) 
        new_client = mqtt.Client()
        new_client.connect(add_node_id+".")
        new_client.loop_start()        
        new_client.publish("/"+add_node_id+"/model/node/add", yaml.dump(my_node), 0, False)
        new_client.disconnect()
        raise cherrypy.HTTPRedirect("/")
    
    
    