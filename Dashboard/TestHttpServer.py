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

import uuid 



class rest:

    @http.expose

    def index(self):

        return """

        <html><body>

        <form method='get' action='/posted'>

        <input value="%s" name="uuid" size='50'/>

        <input type='submit' value='Submit' />

        </form></body>

        </html>

        """ % uuid.uuid4()



    @http.expose

    def posted(self, uuid):

        return """

        <html><body>

        <p>%s</p>

        </body>

        </html>

        """ % uuid

        

if __name__ == "__main__":

    http.config.update( {'server.socket_host':"0.0.0.0", 'server.socket_port':8181 } )

    http.quickstart( rest() )
