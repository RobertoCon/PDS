'''
Created on 01 nov 2016

@author: Conny
'''
from Dev.Factory import Factory
import time
import string
import random

def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def location_generator():
    return random.choice(["bathroom","bedroom","living","kitchen","closet","patio","downstair","box","garden","hall"])

for i in range(0,1) :
    Factory.new_active_light_sensor(id_generator(), location_generator())
Factory.new_active_hue("hue1", "bathroom")
      
'''        
t1= Factory.new_active_temp_sensor("term1", "bath")
t2= Factory.new_active_temp_sensor("term2", "bed")
t3= Factory.new_active_temp_sensor("term3", "liv")
t4= Factory.new_active_temp_sensor("term4", "kitch")
t5=Factory.new_active_hue("hue1", "bath")
t6=Factory.new_active_hue("hue2", "bed")
t7=Factory.new_active_hue("hue3", "liv")
t8=Factory.new_active_hue("hue4", "kitch")           
while True: 
    time.sleep(0.1)
'''            