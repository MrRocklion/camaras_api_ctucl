import sqlite3
import threading
from datetime import datetime
import json


class SqliteManager(threading.Thread):
    def __init__(self,rs232, stop_event):
        super().__init__()
        self.rs232 = rs232
        self.stop_event = stop_event
        self.create_tables()
        self.aux_validation_target = 0
        self.uuid = "799fcd19-23b6-4a00-bed8-8ccc852a4758"
        self.place = "Parada de prueba"
        self.lat = "0.0"
        self.lon = "0.0"

    def run(self):
        while not self.stop_event.is_set():
            with self.rs232.lock:
                if self.rs232.validation:
                    if self.rs232.n_validations != self.aux_validation_target:
                        try:
                            aux_data = str(self.rs232.data[1:-1])
                            current_datetime = datetime.now()
                            data_time = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
                            codigo =aux_data[25:34]
                            tipo = int(aux_data[14:18])
                            fecha = aux_data[6:8]+'/'+aux_data[8:10]+'/'+aux_data[10:14]
                            tiempo = aux_data[0:2]+':'+aux_data[2:4]+':'+aux_data[4:6]
                            costo = float(int(aux_data[46:54])/100)
                            saldo = float(int(aux_data[-8:])/100)
                            saldo_anterior = float(int(aux_data[38:46])/100)
                            self.insert_transaction((codigo,tipo,fecha,tiempo,self.place,costo,saldo_anterior,saldo,self.uuid,self.lat,self.lon,data_time,0))
                            self.aux_validation_target = self.rs232.n_validations
                            print(f'transaccion exitosa! CODIGO:{codigo}')
                        except:
                            print("Hubo un error al momento de registrar la transaccion")

    def add_transaction(self,conn, transaction):
        sql = ''' INSERT INTO transactions(code,type,date_card,time_card,place,cost,previous,balance,uuid,lat,lon,date,upload)
                VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, transaction)
        conn.commit()
        return cur.lastrowid

    def get_transactions(self):
        with sqlite3.connect('app.db') as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM transactions")
            filas = cursor.fetchall()
            nombres_columnas = [descripcion[0] for descripcion in cursor.description]
            resultado = [dict(zip(nombres_columnas, fila)) for fila in filas]
            return resultado
    def get_last_transactions(self):
        with sqlite3.connect('app.db') as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM transactions ORDER BY date DESC LIMIT 10")
            filas = cursor.fetchall()
            nombres_columnas = [descripcion[0] for descripcion in cursor.description]
            resultado = [dict(zip(nombres_columnas, fila)) for fila in filas]
            return resultado

    def create_tables(self):
        sql_statements = [ 
            """CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    code text    NOT NULL,
                    type text    NOT NULL,
                    date_card text NOT NULL,
                    time_card text NOT NULL,
                    place   text  NOT NULL,
                    cost real    NOT NULL,
                    previous real NOT NULL,
                    balance real NOT NULL,
                    uuid text    NOT NULL,
                    lat text NOT NULL,
                    lon text NOT NULL,
                    date timestamp NOT NULL,
                    upload INTEGER NOT NULL DEFAULT 0
            );""",
             """
                CREATE TABLE IF NOT EXISTS gps (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    lat TEXT NOT NULL,
                    lon TEXT NOT NULL,
                    date TEXT NOT NULL,
                    time TEXT NOT NULL,
                    place TEXT NOT NULL,
                    upload INTEGER NOT NULL DEFAULT 0
                );
            """
            ]

        try:
            with sqlite3.connect('app.db') as conn:
                cursor = conn.cursor()
                for statement in sql_statements:
                    cursor.execute(statement)
                conn.commit()
        except sqlite3.Error as e:
            print("OCURRIO ALGO")
            print(e)
    def add_gps_point(self,conn,gps_point):
        sql = ''' INSERT INTO gps(lat,lon,date,time,place,upload)
                VALUES(?,?,?,?,?,?) '''
        cur = conn.cursor()
        cur.execute(sql, gps_point)
        conn.commit()
        return cur.lastrowid

        
    def insert_gps_point(self,_data):
        try:
            with sqlite3.connect('app.db') as conn:
                self.add_gps_point(conn, _data)
        except sqlite3.Error as e:
            print(e)

    def insert_transaction(self,_data):
        try:
            with sqlite3.connect('app.db') as conn:
                transaction_id = self.add_transaction(conn, _data)
                print(f'ID: {transaction_id}')
        except sqlite3.Error as e:
            print(e)

