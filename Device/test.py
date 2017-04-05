'''
Created on 05 apr 2017

@author: Conny
'''
import sched, time
s = sched.scheduler(time.time, time.sleep)
def do_something1(sc): 
    print ("Doing stuff...")
    # do your stuff
    s.enter(1, 1, do_something1, (sc,))
    
def do_something2(sc): 
    print ("Doing stuff      2      ...")
    # do your stuff
    s.enter(5, 1, do_something2, (sc,))

s.enter(1, 1, do_something1, (s,))
s.enter(5, 1, do_something2, (s,))
s.run()