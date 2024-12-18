from flask import Flask, render_template, request,jsonify
import threading
from rs232 import rs232Comunication
from database.SqliteManager import SqliteManager
from FirebaseManager import FirebaseUpload
from GpsManager import Gps
from flask_cors import CORS
import time
from datetime import datetime
app = Flask(__name__)
CORS(app)
stop_event = threading.Event()
#/dev/ttyACM0
@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    return render_template('home.html', result=result)


@app.route('/api/database', methods=['GET', 'POST'])
def db_Api():
    if request.method == 'GET':
        operation = request.args.get('operation')
        if operation == "transactions":
            return  database.get_transactions()
        elif operation == "last_transactions":
            result = database.get_last_transactions()
            print(result)
            return  jsonify({'result':result})
        elif operation == "parameters":
            return database.get_parameters()
        else:
            return 'bad request!', 400
    elif request.method == 'POST':
        params = request.get_json()
        if not params:
            return jsonify({"error": "No se recibió JSON"}), 400
        try:
            date = datetime.now()
            _data = (
                     params['place'],date,params['uuid']
                     )

            database.uuid = params['uuid']
            database.place = params['place']
            database.insert_parameter(_data)
        except:
            return jsonify({"message": "No se recibió JSON Adecuadamente"}), 400
        
        return jsonify({"message": "Datos recibidos"}), 200

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
        fecha_actual = time.strftime("%Y-%m-%d")
        hora_actual = time.strftime("%H:%M:%S")
        new_point = (lat,lon,fecha_actual,hora_actual,database.place,0)
        database.insert_gps_point(new_point)
        point = [float(lat),float(lon)]
        Firebase.update_gps_data(point=point,id=database.uuid)
        return jsonify({"message": "Datos recibidos correctamente"}), 200
    
    except Exception as e:
        print(f"Error al procesar la solicitud: {e}")
        return jsonify({"error": "Ocurrió un error al procesar los datos"}), 500

if __name__ == "__main__":
    rs232 = rs232Comunication(stop_event=stop_event,com='/dev/ttyACM0')
    database = SqliteManager(stop_event=stop_event,rs232=rs232)
    Firebase =  FirebaseUpload(stop_event=stop_event)
    Gps = Gps()
    init_params = database.currentParameters()
    if init_params != None:
        database.place = init_params[1]
        database.uuid = init_params[3]
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