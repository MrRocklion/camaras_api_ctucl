import firebase_admin
import threading
import sqlite3
import time
import uuid
from firebase_admin import credentials,firestore
cred = credentials.Certificate("credentials.json")
app = firebase_admin.initialize_app(cred)
db = firestore.client()


class FirebaseUpload(threading.Thread):
    def __init__(self, stop_event):
        super().__init__()
        self.stop_event = stop_event
    
    def run(self):
        while not self.stop_event.is_set():
            data = self.get_transactions()
            for transaction in data:
                self.loadFirebase(transaction)
            time.sleep(40)

    def get_transactions(self):
        with sqlite3.connect('app.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM transactions WHERE upload = 0")
            filas = cursor.fetchall()
            nombres_columnas = [descripcion[0] for descripcion in cursor.description]
            resultado = [dict(zip(nombres_columnas, fila)) for fila in filas]
            return resultado
    def loadFirebase(self,data):
        id_generate = uuid.uuid4()
        try:
            db.collection("transactions").document(str(id_generate)).set(data)
            self.update_upload_status(data['id'])
        except Exception as e:
            print(e)
            print("falla al subir datos !")

    def update_upload_status(self,id):
        with sqlite3.connect('app.db') as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("UPDATE transactions SET upload = 1 WHERE id = ?", (id,))
                conn.commit()
            except sqlite3.Error as e:
                print(f"Error al actualizar la fila: {e}")