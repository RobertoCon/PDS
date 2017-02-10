'''
Created on 06 gen 2017

@author: Conny
'''
from Model.ApplicationManager import ApplicationManager
from Model.DeviceManager import DeviceManager
from Model.NodeManager import NodeManager
from Model.LoadManager import LoadManager
import cherrypy
#import  subprocess
import time
#import os
from Dashboard.HttpServer import Dashboard

if __name__ == '__main__':
    #check for update
    #update=subprocess.Popen("sudo git -C /opt/pds pull  " , stdout=subprocess.PIPE, shell=True)
    #update.wait()
    #if update.returncode!=0:
    #    exit(-1)
    #boot
    n=NodeManager()
    d=DeviceManager()
    a=ApplicationManager()
    l=LoadManager()
    
    #dashboard
    #http.config.update( {'server.socket_host':"0.0.0.0", 'server.socket_port':8181 } )
    #http.quickstart(Dashboard())
    
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    cherrypy.config.update({'server.socket_port': 8181})
    cherrypy.quickstart(Dashboard())
    #sleep
    while True:
        time.sleep(1)