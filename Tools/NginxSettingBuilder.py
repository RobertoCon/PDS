'''
Created on 20 gen 2017

@author: Conny
'''
from pathlib import Path
from Model import Setting
import yaml

class NginxSettingBuilder(object):

    def __init__(self):
        self.default="""worker_processes  1;
events {
    worker_connections  1024;
}

http {
    include       mime.types;
    default_type  application/octet-stream;
    sendfile        on;
    keepalive_timeout  65;
    server {
        listen       80;
        server_name  localhost;
        location / {
            root   html;
            index  index.html index.htm;
        }
        error_page   500 502 503 504  /50x.html;
        location = /50x.html {
            root   html;
        }
    }
}\n\n"""
        
        self.balancers={}
        self.path = Path(Setting.path+"../Settings/").absolute()
        self.path=self.path.joinpath("LoadRegistry.yaml")
        if self.path.is_file() == False :
            yaml.dump(self.balancers,open(str(self.path),'w')) 
        else:
            self.balancers=yaml.load(open(str(self.path),'r'))
            #build load balancer setting
            for app in self.balancers['node_templates']:
                    server="\tserver {\n\t\tlisten\t"+str(self.balancers['node_templates'][app]['properties']['ports']['in_port']['target'])\
                    +";\n\t\tproxy_pass "+self.balancers['node_templates'][app]['name']+";\n\t}"
                    
                    stream="\tupstream "+self.balancers['node_templates'][app]['name']+"{\n"
                    for link in self.balancers['node_templates'][app]['requirements']['application']:
                        ip=self.balancers['node_templates'][app]['requirements']['application'][link]['ip_address']
                        port=str(self.balancers['node_templates'][app]['requirements']['application'][link]['properties']['ports']['in_port']['target'])
                        stream=stream+"\t\tserver "+ip+":"+port+";\n"
                    stream=stream+"\t}"
                    settings="stream {\n"+server+"\n"+stream+"\n}"
                    
                    
                    print(self.default+settings) 

           
        
NginxSettingBuilder()

#for link in self.balancers['node_templates'][app]['requirements']['application']:
#    ip:self.balancers['node_templates'][app]['requirements']['application'][link]['ip_address']
#port:self.balancers['node_templates'][app]['requirements']['application'][link]['properties']['ports']['in_port']['target']

'''
server="\tserver {\n\t\tlisten\t"+str(self.balancers['node_templates'][app]['properties']['ports']['in_port']['target'])\
                    +" "+self.balancers['node_templates'][app]['properties']['ports']['in_port']['protocol']\
                    +";\n\t\tproxy_pass "+self.balancers['node_templates'][app]['name']+";\n\t}"
                    
                    stream="\tupstream "+self.balancers['node_templates'][app]['name']+"{\n"
                    for link in self.balancers['node_templates'][app]['requirements']['application']:
                        ip=self.balancers['node_templates'][app]['requirements']['application'][link]['ip_address']
                        port=str(self.balancers['node_templates'][app]['requirements']['application'][link]['properties']['ports']['in_port']['target'])
                        stream=stream+"\t\tserver "+ip+":"+port+";\n"
                    stream=stream+"\t}"
                    settings="stream {\n"+server+"\n"+stream+"\n}"
'''