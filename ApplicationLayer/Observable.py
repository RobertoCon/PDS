'''
Created on 22 nov 2016

@author: Conny
'''
import copy

class Observable(object):
        def __init__(self,id_dev,dev,lock_id,state):
            self.id_dev=id_dev
            self.dev=dev
            self.history=[]
            #self.history.append(dev)

            #self.dev=self.dev[len(self.dev)-self.history_size:]
            #self.history=[]
            self.lock_id=lock_id
            self.state=state
            self.obs=[]
            self.history_size=3
            
        def notify_update(self):
            for i in self.obs:
                i.notify_update()
        #def get_observer(self):
        #    observer=Observer(self.dev)
        #    self.obs.append(observer)
        #    return observer
        def update(self,serial_dev,lock_id,state):
            #change this to support history sample
            #self.dev.from_json(serial_dev)
            
            self.history.append(copy.copy(self.dev))
            if len(self.history)>self.history_size:
                self.history=self.history[len(self.history)-self.history_size:]
            self.dev=self.dev.from_json(serial_dev)
            self.lock_id=lock_id
            self.state=state
            self.notify_update()
            
        def observer(self,observer):
            self.obs.append(observer)
            
        def history_size(self,size):
            if size>=1:
                if size<self.history_size:
                    self.history=self.history[len(self.history)-size:]
                self.history_size=size
                return True
            return False
        
        def get_history(self):
            return copy.copy(self.history)

        