'''
Created on 26 ott 2016

@author: Conny
'''
from functools import partial
from Model import Setting
from Device.MqttClient import MqttClient
import threading
import json
from Device.DeviceJobPool import DeviceJobPool

class ActiveDevice(object):

    def __init__(self,dev,runnable=None,handlers=[],broker_ip=Setting.getBrokerIp()):
        
        super(ActiveDevice, self).__init__()
        self.isAlive=True
        self.pool=DeviceJobPool()
        self.dev=dev
        self.locker=threading.RLock()
        self.lock_id=""
        self.lock_stack=[]
        self.client = MqttClient()
        self.runnable=runnable
        self.handlers=handlers
        
        def lock(message , act):
            with self.locker:
                self.lock_stack.append(message['client_id'])
                if act.lock_id=="":
                    act.lock_id=self.lock_stack.pop()
                    act.publish()
                
        def unlock(message , act):
            with self.locker:
                for item in enumerate(self.lock_stack):
                    if message['client_id']==item:
                        self.lock_stack.remove(item)
                if message['client_id']==act.lock_id:
                    if len(self.lock_stack)>0 :
                        act.lock_id=self.lock_stack.pop()
                    else:
                        act.lock_id=""
                    act.publish()
                 
        def update(message , act):
            with self.locker:
                act.publish()

        def write_wrapp(client, userdata, message , act , func):
            json_frame=json.loads(str(message.payload.decode("utf-8")))
            if json_frame['client_id']==act.lock_id or act.lock_id=="":
                with self.locker:
                    func(json_frame,act)
               
               
        for i in handlers:
            self.client.subscribe(i[0],0,partial(write_wrapp,act=self,func=i[1])) 
        self.client.subscribe("/device/"+self.dev.id+"/lock",0,partial(write_wrapp,act=self,func=lock))
        self.client.subscribe("/device/"+self.dev.id+"/unlock",0,partial(write_wrapp,act=self,func=unlock))
        self.client.subscribe("/device/"+self.dev.id+"/update",0,partial(write_wrapp,act=self,func=update))   
        partial(self.runnable,act=self)
        
        self.pool.schedule(self.runnable, self.dev.time_resolution, self)
        
    def publish(self):
        with self.locker:
            struct=[]
            struct.append(self.dev.id)
            struct.append("online")
            struct.append(self.lock_id)
            struct.append(self.dev.to_text())
            self.client.publish(self.dev.topic(),json.dumps(struct),0,retain=True)  

    def terminate(self):
        with self.locker:
            self.isAlive=False
            self.client.publish(self.dev.topic(),'["'+self.dev.id +'","offline","",""]', 0, True) 
            for i in self.handlers:
                self.client.unsubscribe(i[0]) 
            self.client.unsubscribe("/device/"+self.dev.id+"/lock")
            self.client.unsubscribe("/device/"+self.dev.id+"/unlock")
            self.client.unsubscribe("/device/"+self.dev.id+"/update")  