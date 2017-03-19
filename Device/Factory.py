'''
Created on 01 nov 2016

@author: Conny
'''
import sys
import importlib
import json

def load_module(modulename):
    mod = None
    try:
        mod = importlib.import_module(modulename)
    except ImportError:
        print("Failed to load {module}".format(module=modulename),file=sys.stderr)
    return mod

class Factory(object):
    
    @staticmethod
    def decode(serial_dev):
        struct=json.loads(serial_dev)
        if type(struct=='dict'):
            module=load_module("DevicePlugin."+struct['type_dev'])
            if module!=None:
                MyClass = getattr(module, struct['type_dev'])
                instance = MyClass()
                instance.from_text(serial_dev)
                return instance
            return None
        else:
            module=load_module("DevicePlugin."+struct[2])
            if module!=None:
                MyClass = getattr(module, struct[2])
                instance = MyClass()
                instance.from_text(serial_dev)
                return instance
            return None
'''    
    @staticmethod
    def decode_yaml(serial_dev):
        devs=yaml.load(serial_dev)
        module=load_module("DevicePlugin."+devs['device_type'])
        if module!=None:
            MyClass = getattr(module, devs['device_type'])
            instance = MyClass()
            instance.from_yaml(serial_dev)
            return instance
        return None
'''