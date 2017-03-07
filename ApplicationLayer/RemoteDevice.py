'''
Created on 21 nov 2016

@author: Conny
'''
class RemoteDevice(object):

    ready=False
    def __init__(self ,device,shadow):

        self.device=device
        self.shadow=shadow
        self.ready=True
        
    def __getattr__(self, name):
        return getattr(self.device,name)
    
    def __setattr__(self, name, value):
        if self.ready:
            result = self.shadow.write(self.device.id,name)
            return result.result()
        else:
            return object.__setattr__(self, name, value)

    def setattr(self,name,value,async=False,callback=None):
        result = self.shadow.write(self.device.id,name,value,callback)
        if async:
            return result
        else:
            return result.result()
        
    def lock(self):
        return self.shadow.lock(self.device.id)
                
    def unlock(self):
        return self.shadow.unlock(self.device.id)
