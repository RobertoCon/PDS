'''
Created on 05 apr 2017

@author: Conny
'''
from Device.Factory import Factory
import json,yaml
import paho.mqtt.client as mqtt
import time
from functools import partial
import threading
import psutil,os
import urllib.request
from threading import Thread
import socket
import http.client

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

def stress(counter):
    while True:
        #start_time= time.perf_counter()
        #start_process = time.process_time()
        read=urllib.request.urlopen("http://raspy3-A:8282").read()
        #elapsed_process = (time.process_time() - start_process)
        #elapsed_time = (time.perf_counter() - start_time)
        #print(" Process Time : ",elapsed_process," Time : ",elapsed_time)
        counter.add(len(read))

    
    
c=Counter()
thread = Thread(target = stress, args = (c, ))
thread.start()
c1=Counter()
thread1 = Thread(target = stress, args = (c1, ))
thread1.start()
c2=Counter()
thread2 = Thread(target = stress, args = (c2, ))
thread2.start()
thread3 = Thread(target = stress, args = (c, ))
thread3.start()
thread4 = Thread(target = stress, args = (c, ))
thread4.start()
thread5 = Thread(target = stress, args = (c, ))
thread5.start()
thread6 = Thread(target = stress, args = (c, ))
thread6.start()
thread7 = Thread(target = stress, args = (c, ))
thread7.start()
thread8 = Thread(target = stress, args = (c, ))
thread8.start()

while True:
    time.sleep(1)
    print("Request : ",c.get_msg()+c1.get_msg()+c2.get_msg())
    c.zero()
    c1.zero()
    c2.zero()





