import math

class Gps():
    def __init__(self):
        super().__init__()
        self.central_point = [0,0]
        self.geo_radius = 3
    def set_gps_point(self,point):
        """
        Evalua si el bus se ha movido del sitio o se mantiene en el mismo lugar, si esta en una posicion
        diferente actualizara la posicion.
        """
        lat_center, lon_center = self.central_point
        distance = self.haversine(lat_center, lon_center, point[0], point[1])
        if distance >= self.geo_radius:
            self.central_point = point
            return True
        else:
            return False
    
    
   
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
    



