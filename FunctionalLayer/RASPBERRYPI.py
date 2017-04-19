'''
Created on 19 apr 2017

@author: Conny
'''
from FunctionalLayer import PDS
    
class RASPBERRYPI(PDS):
    def __init__(self,dev_id="+",dev_type="RaspberryPi",dev_location="+",shadow=True,starter=None,remote=True):
        super(RASPBERRYPI, self).__init__(dev_id,dev_type,dev_location,shadow,starter,remote)