'''
Created on 19 nov 2016

@author: Conny
'''
from Dev.Factory import Factory
import time
import string
import random
import json

structure = ['{"id":"dev1", "location":"bedroom" , "type":"PluginDevice"}', 
             '{"id":"dev2", "location":"living" , "type":"PluginDevice"}',  
             '{"id":"dev3", "location":"closet" , "type":"PluginDevice"}',
             '{"id":"dev4", "location":"patio" , "type":"PluginDevice"}',  
             '{"id":"dev5", "location":"bathroom" , "type":"Hue", "light":true}', 
             '{"id":"dev6", "location":"kitchen" , "type":"TempSensor", "temperature":0 , "unit":"celsius"}', 
            ]


class Loader(object):

    def __init__(self):

        dev=[]
        for elem in structure:
            device=Factory.decode(elem)
            if device!=None:
                dev.append(device)
                type(device).make_active(device)
        for i in dev:
            print(i.to_json())   
     
     
Loader()
