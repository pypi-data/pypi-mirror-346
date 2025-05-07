import sqlite3
import csv
import os

DB_PATH = os.path.join(os.path.expanduser("~"), ".ubigeo_peru.db")
CSV_PATH = os.path.join(os.path.dirname(__file__), "ubigeo.csv")

def init_database(force=False):
    
    if os.path.exists(DB_PATH):
        if force:
            os.remove(DB_PATH)  
        else:
            return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Crear la tabla UBIGEO
    cursor.execute("""
    CREATE TABLE ubigeo (
        Ubigeo TEXT PRIMARY KEY,
        Distrito TEXT,
        Provincia TEXT,
        Departamento TEXT
    )
    """)

   
    with open(CSV_PATH, newline='', encoding='latin-1') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            cursor.execute("""
            INSERT INTO ubigeo (Ubigeo, Distrito, Provincia, Departamento)
            VALUES (?, ?, ?, ?)
            """, (row['Ubigeo'], row['Distrito'], row['Provincia'], row['Departamento']))

    conn.commit()
    conn.close()
