
import paho.mqtt.client as mqtt
import time
from functools import partial
import threading

    
class Counter(object):
    def __init__(self):
        self.counter=0
        self.locker=threading.RLock()

    def add(self,int_num):
        with self.locker:
            self.counter=self.counter+int_num
            return self.counter
    
    def get(self):
        with self.locker:
            return self.counter
    
    def zero(self):
        with self.locker:
            self.counter=0
    
    
    
def on_message(client, userdata, message,counter):
        print("Received '" +"'   message  '"+ str(message.payload) + "' on topic '"+ message.topic + "' with QoS " + str(message.qos))
        counter.add(len(str(message.payload)))
        
c=Counter()
client = mqtt.Client()
client.connect('192.168.1.8')
client.loop_start()
client.on_message = partial(on_message,counter=c)
client.subscribe("/device/dev1/+/+", qos=0)
while True:
    time.sleep(1)
    print("Speed : ",c.get()," Byte/s")
    c.zero()