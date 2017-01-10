'''
Created on 26 ott 2016

@author: Conny
'''

#Node properties:
node_id="id1"
node_type="Compute"
num_cpus="1" 
disk_size="14 GB"
mem_size="512 MB"
node_ip="192.168.1.6"
# Operating System properties
architecture="ARM" 
os_type="linux"
os_distribution="jessie"
os_version="8.0"
# Framework properties  
path="./"
Broker_ip="192.168.1.6"

'''

node_templates:
      node_id : ID
      type: Pi-Model
      capabilities:
        # Host properties
        host:
          properties:
            num_cpus: 1 
            disk_size: 14 GB
            mem_size: 512 MB
        # Operating System properties
        os:
          properties:
            # Operating System image properties
            architecture: ARM 
            type: linux  
            distribution: jessie  
            version: 8.0  
'''