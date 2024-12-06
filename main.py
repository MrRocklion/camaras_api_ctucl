from flask import Flask, render_template, request,jsonify
import threading
from rs232 import rs232Comunication
from database.SqliteManager import SqliteManager
from FirebaseManager import FirebaseUpload
from GpsManager import Gps
import time
app = Flask(__name__)
stop_event = threading.Event()

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    return render_template('home.html', result=result)


@app.route('/api/database/transactions', methods=['GET'])
def transactions():
    result = None
    return render_template('home.html', result=result)

@app.route('/api/database/counters', methods=['GET'])
def counters():
    result = None
    return render_template('home.html', result=result)

@app.route('/api/gps', methods=['POST'])
def receive_gps_data():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No se enviaron datos JSON"}), 400
        lat = data.get('lat')
        lon = data.get('lon')
        if lat is None or lon is None:
            return jsonify({"error": "Datos incompletos: faltan 'lat' o 'lon'"}), 400
        if lat == 'none' or lon =='none':
            return jsonify({"error": "Datos incompletos: faltan 'lat' o 'lon'"}), 400
        print(f"Latitud: {lat}, Longitud: {lon}")
        fecha_actual = time.strftime("%Y-%m-%d")
        hora_actual = time.strftime("%H:%M:%S")
        new_point = (lat,lon,fecha_actual,hora_actual,'RT-1505',0)
        database.insert_gps_point(new_point)
        point = [float(lat),float(lon)]
        flag = Gps.set_gps_point(point=point)
        if flag:
            Firebase.update_gps_data(point=point)
        return jsonify({"message": "Datos recibidos correctamente"}), 200
    
    except Exception as e:
        print(f"Error al procesar la solicitud: {e}")
        return jsonify({"error": "Ocurrió un error al procesar los datos"}), 500

if __name__ == "__main__":
    rs232 = rs232Comunication(stop_event=stop_event,com='COM6')
    database = SqliteManager(stop_event=stop_event,rs232=rs232)
    Firebase =  FirebaseUpload(stop_event=stop_event)
    Gps = Gps()
    rs232.start()
    database.start() 
    Firebase.start()
    try:
        app.run(host='0.0.0.0', port=5000,use_reloader=False)
    finally:
        stop_event.set()
        rs232.join()
        database.join()
        Firebase.join()
        print("programa terminado!")