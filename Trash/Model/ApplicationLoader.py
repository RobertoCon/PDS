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
    cmd=json_frame['cmd']
    appl=json.loads(json_frame['appl'])
    id_app=appl['app_name']
    
    obj.locker.acquire()
    if cmd=="run":
        #check unique id
        obj.app[id_app]=appl
        obj.app[id_app]['online']="yes"
        obj.docker_run(appl)
    elif cmd=="start":
        obj.app[id_app]=appl
        obj.app[id_app]['online']="yes"
        obj.docker_start(appl)
    elif cmd=="stop":
        obj.app[id_app]=appl
        obj.app[id_app]['online']="no"
        obj.docker_stop(appl)
    elif cmd=="update":
        obj.app[id_app]=appl
        obj.app[id_app]['online']="yes"
        obj.docker_update(appl)
    elif cmd=="regist":
        obj.app[id_app]=appl
        obj.app[id_app]['online']="no"
        
        
    #print all
    #for appl in self.app:
    print("Application table : /n"+json.dumps(obj.app))
                    
    #update permanent file
    obj.permanent()
    obj.locker.release()

class ApplicationLoader(object):

    def __init__(self):
        self.locker=threading.RLock()
        
        
        self.path = Path(Setting.path+"/Settings/").absolute()
        #self.path.mkdir(parents=True, exist_ok=True)
        self.path=self.path.joinpath("application_registry.json")
        
        self.app={}
        if self.path.is_file() == False :
            json.dump(self.app,open(str(self.path),'w')) 
        else:
            #read it
            self.app=json.load(open(str(self.path),'r'))
            for appl in self.app:
                if self.app[appl]['boot']=='yes':
                    self.docker_start(self.app[appl])

        
        self.client = mqtt.Client()
        self.client.connect(Setting.Broker_ip)
        self.client.on_message = partial(on_message, obj=self)
        self.client.loop_start()        
        self.client.subscribe("/application/registry/"+Setting.node_id, qos=0)
        
        
                
       
        time.sleep(1)
 
    def list_app(self):
        return self.app
    
    def permanent(self):
        json.dump(self.app,open(str(self.path),'w'))
    
    #"docker run -it --rm --cpu-quota=30000  --name my-running-app test-python"      
    def docker_run(self,app_json):
        #print("Docker CMD : docker run --cpu-quota="+app_json['cpu_quota']+" --name "+app_json['app_name']+" "+app_json['image_name'])
        proc = subprocess.Popen("docker run --cpu-quota="+app_json['cpu_quota']+" --name "+app_json['app_name']+" "+app_json['image_name'], stdout=subprocess.PIPE, shell=True)
    
    def docker_start(self,app_json):
        #print("Docker CMD : docker start "+app_json['app_name'] )
        proc = subprocess.Popen("docker start "+app_json['app_name'] , stdout=subprocess.PIPE, shell=True)
    
    def docker_stop(self,app_json):
        #print("Docker CMD : docker stop "+app_json['app_name'] )
        proc = subprocess.Popen("docker stop "+app_json['app_name'] , stdout=subprocess.PIPE, shell=True)
    
    def docker_update(self,app_json):
        #print("Docker CMD : docker update --cpu-quota="+app_json['cpu_quota']+" --name "+app_json['app_name'])
        proc = subprocess.Popen("docker update --cpu-quota="+app_json['cpu_quota']+" "+app_json['app_name'], stdout=subprocess.PIPE, shell=True)
    
            
'''
  def new_app(self,data):
        self.app.append(data)
        json.dump(self.app,open(str(self.path),'w')) 
        self.path = Path(Setting.path+"/Application/").absolute()
        self.path=self.path.joinpath(data)
        x = subprocess.Popen("python "+str(self.path), stdout=subprocess.PIPE, shell=True)
        return x
        #Run app
'''       