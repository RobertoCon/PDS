'''
Created on 21 nov 2016

@author: Conny
'''
class RemoteDevice(object):
    '''
    classdocs
    '''
    ready=False
    def __init__(self ,device,read_only=True,shadow=None):
        '''
        Constructor
        '''
        self.device=device
        self.read_only=read_only
        self.shadow=shadow
        self.ready=True
        
    def __getattr__(self, name):
        return getattr(self.device,name)
    
    def __setattr__(self, name, value):
        #print("Set attrib : ",name," at ",value)
        if self.ready:
            if not(self.read_only) :
                setattr(self.device, name,value)
                if self.shadow!=None:
                    self.shadow.write(self.device.id,name,value)
        else:
            return object.__setattr__(self, name, value)  
        
    def lock(self):
        if not(self.read_only) and self.shadow!=None:
                return self.shadow.lock(self.device.id)
        return False
                
    def unlock(self):
        if not(self.read_only) and self.shadow!=None:
            return self.shadow.unlock(self.device.id)
        return False
