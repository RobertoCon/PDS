'''
Created on 29 ott 2016

@author: Conny
'''
from functools import partial
from Model import Setting
import paho.mqtt.client as mqtt
import Pyro4
import _thread
#from Dev import Factory
import json

print("Start")

def getPDScopy(host='localhost'):
    return Pyro4.Proxy("PYRONAME:ShadowBroker").getPDS()
    

def on_message(client, userdata, message , data):
    #data.append(Factory.decode(json.loads(str(message.payload.decode("utf-8")))))
    print("Got new mqtt message")

@Pyro4.expose
class ShadowBroker(object):
    def __init__(self):
        #Device Pool
        print("1")
        self.data=[]
        
        #Mqtt connection
        self.client = mqtt.Client()
        self.client.connect(Setting.Broker_ip)
        self.client.loop_start()
        self.client.on_message = partial(on_message, data=self.data)
        self.client.subscribe("/device/+", qos=0)
        self.client.loop_start()
        print("2")
        

        #Pyro4 bulk
        try:
            self.name_server = Pyro4.locateNS() 
        except:
            try:
                _thread.start_new_thread( Pyro4.naming.startNSloop , ('localhost',) )
                self.name_server = Pyro4.locateNS() 
            except:
                print ("Error: unable to start thread")
                exit()
        print("3")       
         
        self.daemon = Pyro4.Daemon()                # make a Pyro daemon
        self.uri = self.daemon.register(self)   # register the greeting maker as a Pyro object
        self.name_server.register("ShadowBroker", self.uri)   # register the object with a name in the name server
        print("Ready to serve")
        self.daemon.requestLoop()                   # start the event loop of the server to wait for calls
            
    def getPDS(self):
        return self.data.copy()

ShadowBroker()




'''
Created on 29 ott 2016

@author: Conny
'''



from functools import partial
from Model import Setting
import paho.mqtt.client as mqtt
import Pyro4
import _thread
from Dev.Factory import Factory
import json
from ApplicationLayer.PDS import PDS


def getPDS(host='localhost'):
    data=Pyro4.Proxy("PYRONAME:ShadowBroker").getPDScopy()   
    devs=PDS()
    for i in data:
        devs.append(Factory.decode(json.loads(i)))
    return devs 

def on_message(client, userdata, message , data):
    print("Received message '" + str(message.payload) + "' on topic '"+ message.topic + "' with QoS " + str(message.qos))
    dev = Factory.decode(json.loads(str(message.payload.decode("utf-8"))))
    if dev != None:
        for i, item in enumerate(data):
            if dev.id==item.id: 
                data[i] = dev
                return
        data.append(dev)
    else:
        id_dev=message.topic.replace("/device/","")
        for i, item in enumerate(data):
            if id_dev==item.id: 
                print("Remove dev id ",id_dev)
                data.remove(item)
                return
       

      

@Pyro4.expose
class ShadowBroker(object):
    def __init__(self):
        #Device Pool
        self.data=[]
        
        #Mqtt connection
        self.client = mqtt.Client()
        self.client.connect(Setting.Broker_ip)
        self.client.loop_start()
        self.client.on_message = partial(on_message, data=self.data)
        self.client.subscribe("/device/+", qos=0)
        self.client.loop_start()
        

        #Pyro4 bulk
        try:
            self.name_server = Pyro4.locateNS() 
        except:
            try:
                _thread.start_new_thread( Pyro4.naming.startNSloop , ('localhost',) )
                self.name_server = Pyro4.locateNS() 
            except:
                print ("Error: unable to start thread")
                exit()      
         
        self.daemon = Pyro4.Daemon()                # make a Pyro daemon
        self.uri = self.daemon.register(self)   # register the greeting maker as a Pyro object
        self.name_server.register("ShadowBroker", self.uri)   # register the object with a name in the name server
        print("Ready to serve")
        self.daemon.requestLoop()                   # start the event loop of the server to wait for calls
            
    def getPDScopy(self):
        ser=[]
        for i in self.data:
            ser.append(i.json())
        return ser


