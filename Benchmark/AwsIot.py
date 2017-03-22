'''
Created on 22 mar 2017

@author: Conny
'''
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import sys
import logging
import time
import getopt
import psutil,os
from _functools import reduce
from functools import partial
import threading

class Counter(object):
    def __init__(self):
        self.start_time= 0
        self.start_process = 0
        self.locker=threading.RLock()

    def start_clock(self):
        with self.locker:
            self.start_time= time.perf_counter()
            self.start_process = time.process_time()
            
    def end_clock(self):
        with self.locker:
            print(self.start_time)
            return (time.process_time() - self.start_process),(time.perf_counter() - self.start_time)
    
    def reset(self):
        with self.locker:
            self.start_time= 0
            self.start_process = 0
        

# Custom MQTT message callback
def customCallback(client, userdata, message, counter):
        print("Received a new message: ")
        print(message.payload)
        print("from topic: ")
        print(message.topic)
        print("--------------\n\n")
        time1,time2=counter.end_clock()
        print("process time : ",time1," elapsed_time :",time2)

# Usage
usageInfo = """Usage:
Use certificate based mutual authentication:
python basicPubSub.py -e <endpoint> -r <rootCAFilePath> -c <certFilePath> -k <privateKeyFilePath>

Use MQTT over WebSocket:
python basicPubSub.py -e <endpoint> -r <rootCAFilePath> -w

Type "python basicPubSub.py -h" for available options.
"""

# Help info
helpInfo = """-e, --endpoint
        Your AWS IoT custom endpoint
-r, --rootCA
        Root CA file path
-c, --cert
        Certificate file path
-k, --key
        Private key file path
-w, --websocket
        Use MQTT over WebSocket
-h, --help
        Help information
"""

# Read in command-line parameters
useWebsocket = False
host = ""
rootCAPath = ""
certificatePath = ""
privateKeyPath = ""
try:
        opts, args = getopt.getopt(sys.argv[1:], "hwe:k:c:r:", ["help", "endpoint=", "key=","cert=","rootCA=", "websocket"])
        if len(opts) == 0:
                raise getopt.GetoptError("No input parameters!")
        for opt, arg in opts:
                if opt in ("-h", "--help"):
                        print(helpInfo)
                        exit(0)
                if opt in ("-e", "--endpoint"):
                        host = arg
                if opt in ("-r", "--rootCA"):
                        rootCAPath = arg
                if opt in ("-c", "--cert"):
                        certificatePath = arg
                if opt in ("-k", "--key"):
                        privateKeyPath = arg
                if opt in ("-w", "--websocket"):
                        useWebsocket = True
except getopt.GetoptError:
        print(usageInfo)
        exit(1)

# Missing configuration notification
missingConfiguration = False
if not host:
        print("Missing '-e' or '--endpoint'")
        missingConfiguration = True
if not rootCAPath:
        print("Missing '-r' or '--rootCA'")
        missingConfiguration = True
if not useWebsocket:
        if not certificatePath:
                print("Missing '-c' or '--cert'")
                missingConfiguration = True
        if not privateKeyPath:
                print("Missing '-k' or '--key'")
                missingConfiguration = True
if missingConfiguration:
        exit(2)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
if useWebsocket:
        myAWSIoTMQTTClient = AWSIoTMQTTClient("basicPubSub", useWebsocket=True)
        myAWSIoTMQTTClient.configureEndpoint(host, 443)
        myAWSIoTMQTTClient.configureCredentials(rootCAPath)
else:
        myAWSIoTMQTTClient = AWSIoTMQTTClient("basicPubSub")
        myAWSIoTMQTTClient.configureEndpoint(host, 8883)
        myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

#Setup counter
c=Counter()

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
myAWSIoTMQTTClient.subscribe("sdk/test/Python", 1, partial(customCallback ,counter=c))
time.sleep(2)

# Publish to the same topic in a loop forever
loopCount = 0
while True:
        c.reset()
        c.start_clock()
        myAWSIoTMQTTClient.publish("sdk/test/Python", "New Message " + str(loopCount), 1)
        loopCount += 1
        time.sleep(1)
        
        
'''
process time :  0.0029891670000000703  elapsed_time : 0.2630672340019373
process time :  0.0027234369999999952  elapsed_time : 0.22828590399876703
process time :  0.002719115999999966  elapsed_time : 0.23319552800967358
process time :  0.0027521339999999617  elapsed_time : 0.22820376801246312
process time :  0.002748958000000079  elapsed_time : 0.2276779879903188
process time :  0.0028415109999999633  elapsed_time : 0.22736152999277692
process time :  0.002895937000000015  elapsed_time : 0.2259212210046826
process time :  0.0028156249999999883  elapsed_time : 0.2344945360091515
'''