'''
Created on 06 gen 2017

@author: Conny
'''
from Dev.DeviceLoader import DeviceLoader
from ApplicationManager.ApplicationLoader import ApplicationLoader
import time

if __name__ == '__main__':
    l=DeviceLoader()
    a=ApplicationLoader()
    #app_json1={'app_name':'testapp1','cpu_quota':'20000','image_name':'test-python'}
    #app_json2={'app_name':'testapp2','cpu_quota':'40000','image_name':'test-python'}
    #a.docker_run(app_json1)
    #a.docker_run(app_json2)
    
    while True:
        time.sleep(1)