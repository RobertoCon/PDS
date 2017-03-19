
import paho.mqtt.client as mqtt
import time
from functools import partial
import threading
import psutil,os

    
class Counter(object):
    def __init__(self):
        self.counter=0
        self.msg=0
        self.locker=threading.RLock()

    def add(self,int_num):
        with self.locker:
            self.counter=self.counter+int_num
            self.msg=self.msg+1
            return self.counter
    
    def get_byte(self):
        with self.locker:
            return self.counter
    
    def get_msg(self):
        with self.locker:
            return self.msg
    
    def zero(self):
        with self.locker:
            self.counter=0
            self.msg=0
    
    
    
def on_message(client, userdata, message,counter):
        #print("Received '" +"'   message  '"+ str(message.payload) + "' on topic '"+ message.topic + "' with QoS " + str(message.qos))
        counter.add(len(str(message.payload)))
        
c=Counter()
client = mqtt.Client()
client.connect('192.168.1.8')
client.loop_start()
client.on_message = partial(on_message,counter=c)
client.subscribe("/device/dev1/+/+", qos=0)
while True:
    time.sleep(1)
    pid = os.getpid()
    py = psutil.Process(pid)
    print("Speed : ",c.get_byte()*8/(1024*1024)," MBit/s   ---   Msg : ",c.get_msg()," msg/s   ----  Cpu :",psutil.cpu_percent(interval=1, percpu=True))
    c.zero()
    
    
    
    
