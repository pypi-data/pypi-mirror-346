import sqlite3
import os

DB_PATH = os.path.join(os.path.expanduser("~"), ".ubigeo_peru.db")

def connect():
    return sqlite3.connect(DB_PATH)

def buscar_por_ubigeo(Ubigeo):
    conn = connect()
    cur = conn.cursor()
    cur.execute("SELECT * FROM ubigeo WHERE Ubigeo = ?", (Ubigeo,))
    row = cur.fetchone()
    conn.close()
    if row:
        return {
            "Ubigeo": row[0],
            "Distrito": row[1],
            "Provincia": row[2],
            "Departamento": row[3]
        }
    return None

