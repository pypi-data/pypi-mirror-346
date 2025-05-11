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
            port=3306,
            user=usuario,
            password=contraseña,
            database=nombre
        )
        return conn

    elif tipo == 'mongodb':
        from pymongo import MongoClient
        if puerto is None:
            puerto = 27017
        cliente = MongoClient(host=host, 
                              port=puerto, 
                              username=usuario, 
                              password=contraseña)
        print("Conectado a MongoDB")
        return cliente[nombre]

    else:
        raise ValueError("Tipo de base de datos no soportado. Usa 'sqlite', 'mysql' o 'mongodb'.")

def Cerrar_conexion(conn):
    """
    Cierra la conexión a la base de datos.

    Parámetros:
    - conn: objeto de conexión

    Retorna:
    - None
    """
    if conn:
        conn.close() 
        
def Insert(conn, data):
   # Verifica el tipo de base de datos con la que estamos trabajando
    if isinstance(conn, sqlite3.Connection):
        print("Conexión exitosa a la base de datos SQL.")
        # Si estamos usando SQLite, podemos trabajar con la conexión de esta manera
        cursor = conn.cursor()
        # Inserta datos en la tabla 'usuarios'
        cursor.execute("INSERT INTO usuarios (nombre, edad) VALUES (?, ?)", data)
        conn.commit()
        print("Datos insertados correctamente en la base de datos SQL.")

        # Consulta los datos insertados
        cursor.execute("SELECT * FROM usuarios")
        resultados = cursor.fetchall()
        for fila in resultados:
            print(f"ID: {fila[0]}, Nombre: {fila[1]}, Edad: {fila[2]}")
    
    elif isinstance(conn, mysql.connector.connection.MySQLConnection):
        print("Conexión exitosa a la base de datos MySQL.")
        # Si estamos usando MySQL, podemos trabajar con la conexión de esta manera
        cursor = conn.cursor()
        # Inserta datos en la tabla 'usuarios'
        cursor.execute("INSERT INTO usuarios (nombre, edad) VALUES (%s, %s)", data)
        conn.commit()
        print("Datos insertados correctamente en la base de datos MySQL.")

        # Consulta los datos insertados
        cursor.execute("SELECT * FROM usuarios")
        resultados = cursor.fetchall()
        for fila in resultados:
            print(f"ID: {fila[0]}, Nombre: {fila[1]}, Edad: {fila[2]}")
            
            

    elif isinstance(conn, Database):
        print("Conexión exitosa a la base de datos NoSQL.")
        print(conn)
        # Si estamos usando MongoDB, podemos trabajar con la base de datos NoSQL de esta manera
        usuarios = conn["usuarios"]  # Supone que estamos trabajando con la colección 'usuarios'

        # Inserta un documento en la colección
        usuarios.insert_one({"nombre": "Ana", "edad": 25})
        print("Datos insertados correctamente en la base de datos NoSQL.")

        # Consulta los documentos insertados
        for usuario in usuarios.find():
            print(f"Nombre: {usuario['nombre']}, Edad: {usuario['edad']}")