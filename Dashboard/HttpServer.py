'''
Created on 16 gen 2017

@author: Conny
'''
from Dashboard.NodeTable import NodeTable
'''
import http.server
import socketserver

PORT = 9000

Handler = http.server.SimpleHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)

print ("serving at port", PORT)
httpd.serve_forever()
'''



'''
import cherrypy
      
class HelloWorld(object):
    def index(self):
        return "Hello World!"
    index.exposed = True
    
    def random(self):
        return "Random Hello World!"
    random.exposed = True

cherrypy.quickstart(HelloWorld())
'''

import cherrypy as http
import yaml
import paho.mqtt.client as mqtt 
from functools import partial
from Model import Setting

class Dashboard(object):

    def __init__(self):
        super(Dashboard,self).__init__()
        self.nodes={'node_templates':""}
        def on_message(client, userdata, message, obj):
            serial_frame=str(message.payload.decode("utf-8"))
            yaml_frame=yaml.load(serial_frame)
            for node in yaml_frame['node_templates']:  
                if node not in obj.nodes['node_templates']:
                    obj.nodes['node_templates'][node]=yaml_frame['node_templates'][node] 
         
        self.client = mqtt.Client()
        self.client.message_callback_add("/+/model/node/status", partial(on_message, obj=self)) 
        self.client.connect(Setting.Broker_ip)
        self.client.loop_start()        
        self.client.subscribe("/+/model/node/status", qos=0)        
    

    @http.expose
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
            </div><!-- /.container -->
            
            
            
             <!-- Bootstrap core JavaScript
            ================================================== -->
            <!-- Placed at the end of the document so the pages load faster -->
            <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>
            <script>window.jQuery || document.write('<script src="../../assets/js/vendor/jquery.min.js"><\/script>')</script>
            <script src="../../dist/js/bootstrap.min.js"></script>
            <!-- IE10 viewport hack for Surface/desktop Windows 8 bug -->
            <script src="../../assets/js/ie10-viewport-bug-workaround.js"></script>
        </body>
        </html>
        """
    @http.expose
    def node(self,id_node,public_address):
        st=yaml.load("""node_templates: 
    %s:
        type: tosca.nodes.Compute
        attributes:
          private_address: %s
          public_address: %s
        capabilities:
          host:
            properties:
              num_cpus: 1
              cpu_frequency : 1.0 GHz
              disk_size: 16 GB
              mem_size: 512 MB
              os:
                properties:
                  architecture: ARMv6 32bit
                  type: linux
                  distribution: jessie
                  version: 8.0  """ % (id_node,public_address,public_address) )
        return """
        <html><body>
        <p>"""+yaml.dump(st)+"""</p>
        </body>
        </html>
        """