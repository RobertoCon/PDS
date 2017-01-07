'''
Created on 07 gen 2017

@author: Conny
'''

import json

msg={'cmd':'run','appl':'{"app_name":"app1","cpu_quota":"10000","image_name":"test-python"}'}
print(msg['cmd'])
print(msg['appl'])
app=json.loads(msg['appl'])
print(app['app_name'])


'''

msg={'cmd':'run',
        'appl':'{
            "app_name":"app1",
            "online":"no"
            "boot":"yes"
            "cpu_quota":"10000",
            "image_name":"test-python"
        }'
    }

'''