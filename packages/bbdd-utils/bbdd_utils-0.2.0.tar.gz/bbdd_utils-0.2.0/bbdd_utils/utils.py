def saludar(nombre):
    return f"Hola, {nombre}! Esta es tu librería personalizada."



def Conector_bbdd(tipo='sqlite', nombre='mi_base_de_datos', host='localhost', puerto=None, usuario=None, contraseña=None):
    """
    Conecta a una base de datos SQL o NoSQL según el tipo especificado.

    Parámetros:
    - tipo: 'sqlite', 'mysql' o 'mongodb'
    - nombre: nombre de la base de datos
    - host, puerto, usuario, contraseña: solo para MySQL y MongoDB

    Retorna:
    - Objeto de conexión (SQLite/MySQL) o cliente (MongoDB)
    """
    if tipo == 'sqlite':
        import sqlite3
        import os
        nombre_db = f"{nombre}.db"

        crear_tabla = not os.path.exists(nombre_db)
        conn = sqlite3.connect(nombre_db)

        if crear_tabla:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usuarios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT NOT NULL,
                    edad INTEGER NOT NULL
                )
            ''')
            conn.commit()

        return conn

    elif tipo == 'mysql':
        import mysql.connector
        conn = mysql.connector.connect(
            host=host,
            user=usuario,
            password=contraseña,
            database=nombre
        )
        return conn

    elif tipo == 'mongodb':
        from pymongo import MongoClient
        if puerto is None:
            puerto = 27017
        cliente = MongoClient(host=host, port=puerto, username=usuario, password=contraseña)
        return cliente[nombre]

    else:
        raise ValueError("Tipo de base de datos no soportado. Usa 'sqlite', 'mysql' o 'mongodb'.")

def cerrar_conexion(conn):
    """
    Cierra la conexión a la base de datos.

    Parámetros:
    - conn: objeto de conexión

    Retorna:
    - None
    """
    if conn:
        conn.close()    