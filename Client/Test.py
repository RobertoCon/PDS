'''
Created on 10 dic 2016

@author: Conny

import time
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=2) as executor:
    future3 = executor.submit(pow, 323, 1235)
    future = executor.submit(time.sleep,5)
    future2 = executor.submit(pow, 323, 1235)
   
        
    while True:
        print(future2.done())
        print(future.done())
        print(future3.done())
        time.sleep(1)
        
'''     
#import yaml
#di=yaml.load('''node_templates: {}\n''')

#print(di)


import json
array=[]
array.append('self.id1')
array.append(True)
array.append(15)

print(json.dumps(array))

back=json.loads(json.dumps(array))
print(back[0])
print(back[1])
print(back[2]+5)

test={}
test['pippo']='pippo'
print(type(back))
print(type(test))