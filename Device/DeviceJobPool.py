'''
Created on 05 apr 2017

@author: Conny
'''
import threading
import sched, time , math  

         
class DeviceJobPool(object):
    class __DeviceJobPool(threading.Thread):            
        def __init__(self): 
            self.locker=threading.RLock()
            self.balancer=0
            self.size_pool=5     
            self.scheduler=[]
            for i in range(self.size_pool):
                self.scheduler.append(ThreadScheduler())
    
        def schedule(self, task, delay,act):
            print("added job in schedule ",self.balancer)
            with self.locker:
                self.scheduler[self.balancer].enter(delay, 1, task, act)
                self.balancer=int(math.fmod((self.balancer+1), self.size_pool))
                print("result:  ",self.balancer)

    instance = None  
    def __init__(self):
        if not DeviceJobPool.instance:
            print("init singleton")
            DeviceJobPool.instance = DeviceJobPool.__DeviceJobPool()
    def __getattr__(self, name):
        return getattr(self.instance, name)
    def __setattr__(self, name):
        return setattr(self.instance, name)




class ThreadScheduler(threading.Thread): 
    def __init__(self): 
        super(ThreadScheduler, self).__init__()
        self.isAlive=True
        self.locker=threading.RLock()    
        self.scheduler=sched.scheduler(time.time, time.sleep)
        self.start()
                
    def run(self):
        def keepAlive(scheduler):
            #print("Alive",random.randint(1,100))
            if self.isAlive:
                self.scheduler.enter(1, 1, keepAlive, (self.scheduler,))  
             
        self.scheduler.enter(1, 1, keepAlive, (self.scheduler,))  
        self.scheduler.run()     
        
    def enter(self,delay,priority,task, active):
        def periodicTask():
            if active.isAlive:
                task()
                self.scheduler.enter(delay, 1, periodicTask)
        self.scheduler.enter(delay, 1, periodicTask)
        
    def kill(self):
        self.isAlive=False
'''    
def asd():
    print("asd")
    
def qwe():
    print("qwe")
   
dev=DeviceJobPool() 

dev.schedule(asd,5)
dev.schedule(qwe,2)
'''