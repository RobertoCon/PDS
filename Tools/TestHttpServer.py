'''
Created on 16 gen 2017

@author: Conny
'''
'''
import http.server
import socketserver

PORT = 9000

Handler = http.server.SimpleHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)

print ("serving at port", PORT)
httpd.serve_forever()
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
