'''
Created on 08 mar 2017

@author: Conny
'''
import json,yaml
from Device.Factory import Factory 
string='''node_templates:
  dev1:
    type_dev: TempSensor
    id: dev1
    location: bathroom
    requirements: {host: raspy3-A}
    type: my.Device.TempSensor'''
    

yaml_frame=yaml.load(string)
for dev in yaml_frame['node_templates']:
#device=Factory.decode(yaml.dump(self.devices['node_templates'][dev]))
    print(yaml_frame['node_templates'][dev])
    device=Factory.decode(json.dumps(yaml_frame['node_templates'][dev]))
    print(device.id)
#device=Factory.decode(json.dumps(yaml.load(self.devices['node_templates'][dev])))     
#print((json.dumps(yaml.load(string)['node_templates']['dev1'])))