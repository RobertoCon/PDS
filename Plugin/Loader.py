'''
Created on 17 nov 2016

@author: Conny
'''
from __future__ import print_function
import sys
import importlib

def load_module(modulename):
    mod = None
    try:
        mod = importlib.import_module(modulename)
    except ImportError:
        print("Failed to load {module}".format(module=modulename),
                     file=sys.stderr)
    return mod