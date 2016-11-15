'''
Created on 25 ott 2016

@author: Conny
'''
from attrdict.dictionary import AttrDict
import json

structure = AttrDict({
        'location_type':{'bathroom' : 'bathroom' , 'kitchen':'kitchen','livingroom':'livingroom','bedroom':'bedroom' },
        'device_type'  :{'sensor_temp' : 'sensor_temp' , 'sensor_light':'sensor_light','switch_light':'switch_light','sensor_move':'sensor_move'},
        'device'       :{
            'sensor_temp':{
                'id':{'name':'id','type':'string' , 'final':True ,'write':False}  ,
                'location':{'name':'location',  'type':'location_type' , 'final':True ,'write':False}   ,  
                'device':{'name':'device', 'type':'sensor_temp' , 'final':True ,'write':False}   ,   
                'temperature':{'name':'temperature', 'type':'float' , 'unit':'celsius' , 'final':False ,'write':False}   , 
                'struct':{'id':'0', 'location':'default' , 'device':'sensor_temp' , 'temperature':0}          
            },
            'sensor_light':{
                'id':{'name':'id', 'type':'string' , 'final':True ,'write':False}  ,
                'location':{'name':'location', 'type':'location_type' , 'final':True ,'write':False}   ,  
                'device':{'name':'device', 'type':'sensor_light' , 'final':True ,'write':False}   ,   
                'light':{'name':'light', 'type':'float' , 'unit':'lumen' , 'final':False ,'write':False}   ,  
                'struct':{'id':'0', 'location':'default' , 'device':'sensor_light' , 'light':0}         
            },
            'sensor_move':{
                'id':{'name':'id',  'type':'string' , 'final':True ,'write':False}  ,
                'location':{'name':'location', 'type':'location_type' , 'final':True ,'write':False}   ,  
                'device':{'name':'device', 'type':'switch_light' , 'final':True ,'write':False}   ,   
                'move_state':{'name':'move_state', 'type':'bool' , 'final':False ,'write':False}   ,
                'struct':{'id':'0', 'location':'default' , 'device':'sensor_move' , 'move_state':False}             
            },
            'switch_light':{
                'id':{'name':'id',  'type':'string' , 'final':True ,'write':False}  ,
                'location':{'name':'location', 'type':'location_type' , 'final':True ,'write':False}   ,  
                'device':{'name':'device', 'type':'switch_light' , 'final':True ,'write':False}   ,   
                'light_state':{'name':'light_state', 'type':'bool' , 'final':False ,'write':False}   ,
                 'struct':{'id':'0', 'location':'default' , 'device':'switch_light' , 'light_state':False}           
            }  
        }
         
})

'''

    
def is_mutable(x):
    if x.final :
        print("immutable")
    else : 
        print("mutable")
        
        

#Sugar
def Device(x):
    return AttrDict(x)

def print_json(x):
    print(json.dumps(x))
  
        
#print empty struct  
print("Empty struct :") 
print_json(structure.device.sensor_temp.struct)


#Create a new object from a struct
print("New Object :")

x=Device(structure.device.sensor_temp.struct)
print_json(x)
x.id='5'
x.location = structure.location_type.bathroom
x.temperature=25
print("Object modified :")
print_json(x)

#Extend the object
def extend(x):
    x.faren=x.temperature+10
    return x

x=extend(x)
print("Object extended :")
print_json(x)



#Define a new type
x=AttrDict(structure.device.sensor_light.struct + structure.device.switch_light.struct)
x.id='10'
x.device='switch_sensor_light'
print("New Type Object switch_light+sensor_light :")
print_json(x)

'''