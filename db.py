import mysql.connector
from mysql.connector import Error

def get_db_connection():

    try:
        connection = mysql.connector.connect(
            host='localhost',  # Cambia según tu configuración
            user='root',       # Usuario de MySQL
            password='password',  # Contraseña de MySQL
            database='mi_base'    # Nombre de la base de datos
        )
        if connection.is_connected():
            print("Conexión a la base de datos establecida")
        return connection
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

def close_db_connection(connection):
    if connection.is_connected():
        connection.close()
        print("Conexión a la base de datos cerrada")
