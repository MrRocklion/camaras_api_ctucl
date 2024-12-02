import paho.mqtt.client as paho
import time
import math
import json

class Gps():
    def __init__(self):
        super().__init__()
        self.topic = 'devices/l2/rt1505'
        self.username = 'monitoreo'
        self.password = 'ctucl2024@'
        self.ca_cert = 'ca.crt'
        self.broker = 'mae21b2a.ala.us-east-1.emqxsl.com'
        self.port = 8883  # SSL/TLS port 
        self.central_point = [0,0]
        self.geo_radius = 3
    def set_gps_point(self,point):
        lat_center, lon_center = self.central_point
        distance = self.haversine(lat_center, lon_center, point[0], point[1])
        if distance >= self.geo_radius:
            self.central_point = point
            self.send_data(point)
        else:
            pass

    def on_connect(self,client, userdata, flags,rc):
        if rc == 0:
            print("Connected to MQTT Broker with SSL/TLS!")
        else:
            print(f"Failed to connect, return code {rc}")
    def send_data(self,point):
        client = paho.Client()
        client.username_pw_set(self.username, self.password)
        client.tls_set(ca_certs=self.ca_cert)
        client.on_connect = self.on_connect
        client.connect(self.broker, self.port)
        client.loop_start()
        fecha_actual = time.strftime("%Y-%m-%d")
        hora_actual = time.strftime("%H:%M:%S")
        message = {
            "lat":point[0],
            "lon":point[1],
            "date":fecha_actual,
            "time":hora_actual
        }
        result = client.publish(self.topic, json.dumps(message))
        time.sleep(1)
        client.loop_stop()
        client.disconnect()
    def haversine(self,lat1, lon1, lat2, lon2):
        """
        Calcula la distancia en metros entre dos puntos GPS usando la fórmula de haversine.
        """
        R = 6371000  # Radio de la Tierra en metros
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)
        # Fórmula de haversine
        a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c
    



