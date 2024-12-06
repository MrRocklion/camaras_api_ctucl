import paho.mqtt.client as paho
import time
import math
import json

def on_connect(self,client, userdata, flags,rc):
    if rc == 0:
        print("Connected to MQTT Broker with SSL/TLS!")
    else:
        print(f"Failed to connect, return code {rc}")
topic = 'devices/l2/rt1505'
username = 'monitoreo'
password = 'ctucl2024@'
ca_cert = 'ca.crt'
broker = 'mae21b2a.ala.us-east-1.emqxsl.com'
port = 8883  # SSL/TLS port 
central_point = [0,0]
geo_radius = 3
client = paho.Client()
client.tls_set(ca_certs=ca_cert)
client.username_pw_set(username, password)
client.on_connect = on_connect
client.connect(broker, port)
client.loop_start()
fecha_actual = time.strftime("%Y-%m-%d")
hora_actual = time.strftime("%H:%M:%S")
message = {
    "lat":-75.17984532,
    "lon":1.17984532,
    "date":fecha_actual,
    "time":hora_actual
}
result = client.publish(topic, json.dumps(message),retain=True)
client.loop_stop()
client.disconnect()