'''
Created on 05 apr 2017

@author: Conny
'''
from Device.Factory import Factory
import json,yaml

devices=[]
for i in range(400):
    dictasd=yaml.load('''
            type_dev: TempSensor
            id_dev: dev1
            location_dev: bathroom
            time_resolution: 1
            timestamp: 0
            requirements: {host: raspy3-A}
            type: my.Device.TempSensor
            temperature: 0
            unit: celsius
            ''')
    print(dictasd)
    devices.append(Factory.decode(json.dumps(dictasd)))
    
print("Fine",len(devices))
    