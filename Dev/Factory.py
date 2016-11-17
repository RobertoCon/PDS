'''
Created on 01 nov 2016

@author: Conny
'''
from Dev.Device import Device
import json
import sys
import importlib

def load_module(modulename):
    mod = None
    try:
        mod = importlib.import_module(modulename)
    except ImportError:
        print("Failed to load {module}".format(module=modulename),file=sys.stderr)
    return mod

class Factory(object):
    
    @staticmethod
    def decode(struct):
        MyClass = getattr(load_module("Plugin."+struct['type']), struct['type'])
        instance = MyClass()
        instance.from_json(struct)
        return instance

'''   

    #print("Decode json : ",json)
        if json['type']=="device":
            return Factory.new_device(json['id'],json['location'],json['type'],json['lock_id'])
        elif json['type']=="temp_sensor":
            return Factory.new_temp_sensor(json['id'],json['location'],json['type'],json['lock_id'],json['temperature'])
        elif json['type']=="hue":
            return Factory.new_hue(json['id'],json['location'],json['type'],json['lock_id'],json['light'])
        elif json['type']=="light_sensor":
            return Factory.new_light_sensor(json['id'],json['location'],json['type'],json['lock_id'],json['light'],json['unit'])
        else:
            return None
 
    @staticmethod
    def new_device(id_dev ,location_dev,type_dev="device",lock_id=""):
            return Device(id_dev, location_dev, type_dev,lock_id)
        
    @staticmethod
    def new_temp_sensor(id_dev ,location_dev,type_dev="temp_sensor",lock_id="",temperature=0):
            return TempSensor(id_dev, location_dev, type_dev,temperature,lock_id)
          
    @staticmethod          
    def new_active_temp_sensor(id_dev ,location_dev,type_dev="temp_sensor",lock_id="",temperature=0):
        def jobToDo(act):
                while True:
                    act.dev.temperature=random.randint(1,30) #Read temp somewhere
                    act.publish()
                    time.sleep(10)
        return ActiveDevice(Factory.new_temp_sensor(id_dev ,location_dev,type_dev,lock_id,temperature),jobToDo,[])
    
    
    @staticmethod
    def new_hue(id_dev ,location_dev,type_dev="hue",lock_id="",light=False):
            return Hue(id_dev, location_dev, type_dev,lock_id,light)
          
    @staticmethod          
    def new_active_hue(id_dev ,location_dev,type_dev="hue",lock_id="",light=False):
        def jobToDo(act):
                while True:
                    act.publish()
                    time.sleep(10)

        #Write status 
        def listener2(client, userdata, message , act):
            print(str(client._client_id))
            if bool(message.payload.decode("utf-8"))==False:
                act.dev.light=False
            elif bool(message.payload.decode("utf-8"))==True:
                act.dev.light=True
            act.publish()
        return ActiveDevice(Factory.new_hue(id_dev ,location_dev,type_dev,lock_id,light),jobToDo,[("/device/"+id_dev+"/light",listener2)])
    
    
    
    
    
    
    
    @staticmethod
    def new_light_sensor(id_dev ,location_dev,type_dev="light_sensor",lock_id="",light=0,unit="lumen"):
            return LightSensor(id_dev, location_dev, type_dev,lock_id,light,unit)
          
    @staticmethod          
    def new_active_light_sensor(id_dev ,location_dev,type_dev="light_sensor",lock_id="",unit="lumen"):
        def jobToDo(act):
                while True:
                    act.dev.light=random.randint(1,100)
                    act.publish()
                    time.sleep(10)
        return ActiveDevice(Factory.new_light_sensor(id_dev ,location_dev,type_dev,lock_id,unit="lumen"),jobToDo,[])
'''
#print ( Factory.decode(json.loads('{"location": "bed", "type": "temp_sensor", "id": "term2", "temperature": 15}')).temperature)