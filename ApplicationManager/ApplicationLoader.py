'''
Created on 19 nov 2016

@author: Conny
'''

from pathlib import Path
import json
from functools import partial
from Model import Setting
import paho.mqtt.client as mqtt
import time
import threading
import  subprocess

def on_message(client, userdata, message, obj):
    serial_frame=str(message.payload.decode("utf-8"))
    json_frame=json.loads(serial_frame)
    key=json_frame['key']
    obj.locker.acquire()
    obj.table[key]=json.loads(json_frame['data'])
    obj.locker.release()

class ApplicationLoader(object):

    def __init__(self):
        self.locker=threading.RLock()
        
        self.client = mqtt.Client()
        self.client.connect(Setting.Broker_ip)
        self.client.on_message = partial(on_message, obj=self)
        self.client.loop_start()        
        self.client.subscribe("/application/registry/"+Setting.node_id, qos=0)
        
        self.path = Path(Setting.path+"/Settings/").absolute()
        self.path.mkdir(parents=True, exist_ok=True)
        self.path=self.path.joinpath("app_registry.json")
        
        self.app=[]
        if self.path.is_file() == False :
            json.dump(self.app,open(str(self.path),'w')) 
        else:
            #read it
            self.app=json.load(open(str(self.path),'r'))
       
        time.sleep(1)
        
    def new_app(self,data):
        self.app.append(data)
        json.dump(self.app,open(str(self.path),'w')) 
        self.path = Path(Setting.path+"/Application/").absolute()
        self.path=self.path.joinpath(data)
        x = subprocess.Popen("python "+str(self.path), stdout=subprocess.PIPE, shell=True)
        return x
        #Run app
        
    def list_app(self):
        return self.app
          
    
        
l=ApplicationLoader()
print(l.list_app())
save=l.new_app("script.py")
print(l.list_app())


def runcmd(cmd):
    x = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    return x.stdout

print(save.stdout)
print("code done")
time.sleep(10)
print(save.stdout.readline())
print("code done 2")




        
        