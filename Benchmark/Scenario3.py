'''
Created on 19 apr 2017

@author: Conny
'''
import cherrypy

class Scen3(object):
    def __init__(self):
        self.counter=0
   
    @cherrypy.expose
    def index(self):
        self.counter=self.counter+1
        return str(self.counter)

cherrypy.config.update({'server.socket_host': '0.0.0.0'})
cherrypy.config.update({'server.socket_port': 9000})
cherrypy.quickstart(Scen3())