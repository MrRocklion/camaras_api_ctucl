import paho.mqtt.client as paho
import time
import math
import json
import firebase_admin
import uuid
from firebase_admin import credentials,firestore
cred = credentials.Certificate("credentials.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()

class Gps():
    def __init__(self):
        super().__init__()
        self.central_point = [0,0]
        self.geo_radius = 3
        self.id_bus = 'rt1505' #este parametro es importante cambiar en cada bus
    def set_gps_point(self,point):
        """
        Evalua si el bus se ha movido del sitio o se mantiene en el mismo lugar, si esta en una posicion
        diferente actualizara la posicion.
        """
        lat_center, lon_center = self.central_point
        distance = self.haversine(lat_center, lon_center, point[0], point[1])
        if distance >= self.geo_radius:
            self.central_point = point
            self.send_data(point)
        else:
            pass
    
    def send_data(self,point):
        """
        Actualiza la latitud y longitud del bus con el id especificado
        """
        fecha_actual = time.strftime("%Y-%m-%d")
        hora_actual = time.strftime("%H:%M:%S")
        data = {
            "lat":point[0],
            "lon":point[1],
            "date":fecha_actual,
            "time":hora_actual
        }
        try:
            db.collection("transactions").document(self.id_bus).update(data)
        except Exception as e:
            print(e)
            print("falla al subir datos !")
   
    def haversine(self,lat1, lon1, lat2, lon2):
        """
        Calcula la distancia en metros entre dos puntos GPS usando la fórmula de haversine.
        """
        R = 6371000 
        phi1 = math.radians(lat1)
        phi2 = math.radians(lat2)
        delta_phi = math.radians(lat2 - lat1)
        delta_lambda = math.radians(lon2 - lon1)
        a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return R * c
    



