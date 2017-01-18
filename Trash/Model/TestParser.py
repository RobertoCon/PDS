'''
Created on 14 gen 2017

@author: Conny
import yaml
document = """
  a: 1
  b:
    c: 3
    d: 4
"""
x=(yaml.load(document))
print(x['b'])
for elem in x['b']:
    print("asd : ",x['b'][elem])
print (yaml.dump(yaml.load(document)))
'''
import yaml
from Dev.Factory import Factory
stream = open('../Settings/example_device.yaml', 'r')
x=(yaml.load(stream))
print(yaml.dump(x))
dev=Factory.decode_yaml(yaml.dump(x))
print(dev)

