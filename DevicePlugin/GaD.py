'''
Created on 16 dic 2016

@author: Conny
'''

from Device.Device import Device
#from Device.ActiveDevice import ActiveDevice
import json


class GaD(Device):

    def __init__(self,id_dev="",location_dev="unknown"):
        super(GaD, self).__init__(id_dev, location_dev, type_dev="GaD")
        self.attr1=0
         
    #redefine how to serialize the struct
    def to_text(self):
        array=[]
        array.append(self.id)
        array.append(self.location)
        array.append(self.type)
        array.append(self.time_resolution)
        array.append(self.attr1)
        return json.dumps(array)
        
    def from_text(self,serial_dict):
        obj=json.loads(str(serial_dict))
        if type(obj)=='list':
            self.id=obj[0]
            self.location=obj[1]
            self.type =obj[2]
            self.time_resolution=obj[3]
            self.attr1=obj[4]
        else:
            self.id = obj['id_dev']
            self.location =obj['location_dev'] 
            self.type=obj['type_dev']
            self.time_resolution=obj['time_resolution']
            self.attr1=obj['attr1']
        return self

    @staticmethod          
    def html(device):
        html=""
        #build html code 
        return html
    
    '''    
    @staticmethod          
    def make_active(device,broker_ip=""):
        #Define Handlers here
            #handlers=[("topic1",function1),("topic2",function2)] like [("/device/"+id_dev+"/light",function)]
        #Define Job to perform periodically
        def job_to_do(active):
            while True:
                #do something
                active.publish()
                time.sleep(10)            
        return ActiveDevice(device,job_to_do,handlers)
'''     