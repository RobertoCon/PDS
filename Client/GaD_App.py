'''
Created on 16 dic 2016

@author: Conny
'''


from ApplicationLayer.PDS import LIGHT
from Device.ActiveDevice import ActiveDevice
import time
from DevicePlugin.GaD import GaD

supernode_ip="192.168.1.5"#"cluster supernode ip"

def job_to_do(active):
    while True:
        #get data from local iot gateway
        devs=LIGHT().filter(lambda x : x.location=="bedroom").filter(lambda x : x.unit=="Lumen")
        
        #update structure
        active.dev.attr1=devs[0].light
        
        #publish to supernode
        active.publish()
        time.sleep(10) 
        
handlers=[]
dev=ActiveDevice(GaD("GaD1","Zone1"),job_to_do,handlers,supernode_ip)


