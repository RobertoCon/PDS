'''
Created on 19 apr 2017

@author: Conny
'''
import cherrypy
import subprocess

class Scen3(object):
    def __init__(self):
        self.host=subprocess.getoutput("hostname")
        self.counter=0
   
    @cherrypy.expose
    def index(self):
        self.counter=self.counter+1
        return str(self.counter)+":"+self.host

cherrypy.config.update({'server.socket_host': '0.0.0.0'})
cherrypy.config.update({'server.socket_port': 9000})
cherrypy.quickstart(Scen3())