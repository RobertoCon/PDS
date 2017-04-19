'''
Created on 19 apr 2017

@author: Conny
'''
from FunctionalLayer.PDS import PDS

class HUE(PDS):
    def __init__(self,dev_id="+",dev_type="Hue",dev_location="+",shadow=True,starter=None,remote=True):
        super(HUE, self).__init__(dev_id,dev_type,dev_location,shadow,starter,remote)