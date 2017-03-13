'''
Created on 06 gen 2017

@author: Conny
'''
from Model.ApplicationManager import ApplicationManager
from Model.DeviceManager import DeviceManager
from Model.NodeManager import NodeManager
from Model.LoadManager import LoadManager
from Dashboard.HttpServer import Dashboard
import cherrypy
import time
#import sys, getopt


#Default mode
NodeManager()
DeviceManager()
ApplicationManager()
LoadManager()
#Dashboard
#cherrypy.config.update({'server.socket_host': '0.0.0.0'})
#cherrypy.config.update({'server.socket_port': 8181})
#cherrypy.quickstart(Dashboard())
#sleep
while True:
    time.sleep(1)

'''
def main(argv):
    try:
        opts, args = getopt.getopt(argv,"h")
    except getopt.GetoptError:
        print ('Error option command : ',args)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            #Helper
            print ('help menu args :',arg)
            sys.exit()
        elif opt== '-b':
            #Benchmark mode
            pass
        elif opt== '-d':
            #Deamon mode
            NodeManager()
            DeviceManager()
            ApplicationManager()
            LoadManager()
        else:
            #Default mode
            NodeManager()
            DeviceManager()
            ApplicationManager()
            LoadManager()
            #Dashboard
            cherrypy.config.update({'server.socket_host': '0.0.0.0'})
            cherrypy.config.update({'server.socket_port': 8181})
            cherrypy.quickstart(Dashboard())
    #sleep
    while True:
        time.sleep(1)
        
if __name__ == '__main__':
    main(sys.argv[1:])
'''