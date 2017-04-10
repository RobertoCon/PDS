'''
Created on 31 ott 2016

@author: Conny
'''

from Device.Device import Device
#from Device.ActiveDevice import ActiveDevice
from Device.ActiveDevicePoolThread import ActiveDevice
import json
import time
import psutil
from _functools import reduce
import subprocess

class RaspberryPi(Device):

    def __init__(self,id_dev="",location_dev="unknown",time_resolution=0.33):
        super(RaspberryPi, self).__init__(subprocess.getoutput("hostname"), location_dev, type_dev="RaspberryPi",time_resolution=time_resolution)
        self.timestamp=time.time()
        self.gps=[0.0,0.0]
        self.cpus=[]
        self.cpu_avg=0
        self.cpu_freq=0
        self.mem_ava=0
        self.mem_tot=0
        self.disk_tot=0
        self.disk_ava=0
        self.hostname=subprocess.getoutput("hostname")
        self.ip=subprocess.getoutput("hostname -i")
        
    def to_text(self):
        array=[]
        array.append(self.id)
        array.append(self.location)
        array.append(self.type)
        array.append(self.time_resolution)
        array.append(self.timestamp)
        array.append(self.gps)
        array.append(self.cpus)
        array.append(self.cpu_avg)
        array.append(self.cpu_freq)
        array.append(self.mem_ava)
        array.append(self.mem_tot)
        array.append(self.disk_tot)
        array.append(self.disk_ava)
        array.append(self.ip)
        array.append(self.hostname)
        return json.dumps(array)

    def from_text(self,serial_dict):
        struct=json.loads(str(serial_dict))
        if type(struct) is list:
            self.id=struct[0]
            self.location=struct[1]
            self.type =struct[2]
            self.time_resolution=struct[3]
            self.timestamp=struct[4]
            self.gps=struct[5]
            self.cpus=struct[6]
            self.cpu_avg=struct[7]
            self.cpu_freq=struct[8]
            self.mem_ava=struct[9]
            self.mem_tot=struct[10]
            self.disk_tot=struct[11]
            self.disk_ava=struct[12]
            self.ip=struct[13]
            self.hostname=struct[14]
        return self
     
    @staticmethod          
    def make_active(device):
        #Define Handlers here
        handlers=[] #[("topic1",function1),("topic2",function2)] like [("/device/"+id_dev+"/light",function)]
        #Define Job to perform periodically
        def job_to_do(active):
                with active.locker:
                    active.cpus=psutil.cpu_percent(interval=1, percpu=True)
                    active.cpu_avg=0=reduce(lambda x,y:(x+y)/2,psutil.cpu_percent(interval=1, percpu=True),0)
                    active.cpu_freq=psutil.cpu_freq()
                    
                    #svmem(total=19318026240, available=15660314624, percent=18.9, used=3657711616, free=15660314624)
                    active.mem_ava=psutil.virtual_memory()[1]
                    active.mem_tot= psutil.virtual_memory()[0]

                    active.disk_tot=psutil.disk_usage('/')[0]
                    active.disk_ava=psutil.disk_usage('/')[2]

     
                    active.dev.timestamp=time.time()
                    active.publish()
                
        return ActiveDevice(device,job_to_do,handlers)
    
    @staticmethod          
    def html(device):
        return 'code'
    
    
    #Latitudine: 45.465454 | Longitudine: 9.186516