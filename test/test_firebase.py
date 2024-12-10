import firebase_admin
import time
from firebase_admin import credentials,firestore
cred = credentials.Certificate("credentials.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()


current_timestamp = int(time.time())
data = {
    "latitud":-3.9986464435892852,
    "longitud":-79.2082797024977,
    "ultima_con":current_timestamp
}
try:
    db.collection("unidades").document('rt1505').update(data)
except Exception as e:
    print(e)
    print("falla al subir datos !")


