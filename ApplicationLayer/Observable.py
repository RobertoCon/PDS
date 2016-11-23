'''
Created on 22 nov 2016

@author: Conny
'''
class Observer(object):
        def __init__(self,dev,shadow):
            self.dev=dev
            self.shadow=shadow
            self.shadow.observer(dev.id,self)
            
        def notify_update(self):
            #do something
            pass

class Observable(object):
        def __init__(self,id_dev,dev,lock_id,state):
            self.id_dev=id_dev
            self.dev=dev
            self.lock_id=lock_id
            self.state=state
            self.obs=[]
        def notify_update(self):
            for i in self.obs:
                i.notify_update()
        def get_observer(self):
            observer=Observer(self.dev)
            self.obs.append(observer)
            return observer
        def update(self,serial_dev,lock_id,state):
            #change this to support history sample
            self.dev.from_json(serial_dev)
            self.lock_id=lock_id
            self.state=state
            
        def observer(self,observer):
            self.obs.append(observer)
        

        