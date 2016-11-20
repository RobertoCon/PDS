'''
Created on 19 nov 2016

@author: Conny
'''
from Dev.Factory import Factory
from Model.Model import structure
import time
import string
import random
import json


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
