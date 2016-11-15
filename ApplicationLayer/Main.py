'''
Created on 01 nov 2016

@author: Conny
'''
from ApplicationLayer.PDS import PDS,TEMP,HUE,LIGHT
import time

'''
x=HUE(shadow=False,starter=[5,10,20])
print(x.filter(lambda x : x <11))
print(x)
y=HUE(shadow=False,starter=[3,5,6,7])
print(x)
print(y.dev_type)
z=HUE("HUE","bath",shadow=False,starter=[5,10,20])
print(z.dev_type)
print(z.filter(lambda x : x < 6))


'''
#x=LIGHT()
#x.print()
print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
#x=LIGHT().filter(lambda x : x.location=="bedroom").map(lambda x:x.light).reduce(lambda x,y:(x+y)/2)
#print(x)
x=HUE()
x[0].lock()
x[0].light=True
x.print()
time.sleep(30)
print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
x=HUE()
x.print()
x[0].unlock()
x=HUE().lock()
x.print()

