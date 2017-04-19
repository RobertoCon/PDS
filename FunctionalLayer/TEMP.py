'''
Created on 19 apr 2017

@author: Conny
'''
from FunctionalLayer.PDS import PDS

class TEMP(PDS):
    def __init__(self,dev_id="+",dev_type="TempSensor",dev_location="+",shadow=True,starter=None,remote=True):
        super(TEMP, self).__init__(dev_id,dev_type,dev_location,shadow,starter,remote)