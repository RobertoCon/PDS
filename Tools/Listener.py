
import paho.mqtt.client as mqtt
import time
from Model import Setting

def on_message(client, userdata, message):
        print("Received '" +"'   message  '"+ str(message.payload) + "' on topic '"+ message.topic + "' with QoS " + str(message.qos))
        
client = mqtt.Client()
client.connect(Setting.Broker_ip)
client.loop_start()
client.on_message = on_message
client.subscribe("#", qos=0)
while True:
    time.sleep(1)
        