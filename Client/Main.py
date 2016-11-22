'''
Created on 01 nov 2016

@author: Conny
'''
from ApplicationLayer.PDS import PDS,TEMP,HUE,LIGHT
import time

#x=LIGHT()
#x.print()
print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
y=LIGHT().filter(lambda x : x.location=="bedroom").map(lambda x:x.light).reduce(lambda x,y:(x+y)/2)
print(y)
x=HUE(remote=True).lock()

#x[0].lock()
x.print()
x[0].light=False
x.print()
#time.sleep(30)
print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
x.print()
#x[0].unlock()
x.unlock()
#x=HUE().lock()
x=HUE()
x.print()


        