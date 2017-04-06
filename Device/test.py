'''
Created on 05 apr 2017

@author: Conny
'''
from Device.Factory import Factory

import json

devices=[]
for i in range(400):
    devices[i]=Factory.decode(json.dumps('''node_templates:
  dev1:
    type_dev: TempSensor
    id_dev: dev1
    location_dev: bathroom
    time_resolution: 1
    timestamp: 0
    requirements: {host: raspy3-A}
    type: my.Device.TempSensor
    temperature: 0
    unit: celsius'''))
    
print("Fine")
    