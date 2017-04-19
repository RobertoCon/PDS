'''
Created on 05 apr 2017

@author: Conny
'''
from Device.Factory import Factory
import json,yaml


    
    
import urllib.request
while True:
    read=urllib.request.urlopen("http://raspy3-A:9000").read()
    print(read)
