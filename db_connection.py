import mysql.connector
from mysql.connector import Error

def get_db_connection():
    """
    Establece una conexión con la base de datos MySQL.
    """
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='ntn3',
         
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

class DatabaseConnection:
    def __enter__(self):
        """
        Método para entrar al contexto con la conexión activa.
        """
        self.connection = get_db_connection()
        if not self.connection:
            raise RuntimeError("No se pudo conectar a la base de datos.")
        self.cursor = self.connection.cursor(dictionary=True)  # Configurar cursor como diccionario
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Método para salir del contexto cerrando la conexión y el cursor.
        """
        if hasattr(self, 'cursor') and self.cursor:
            self.cursor.close()
        if self.connection and self.connection.is_connected():
            self.connection.close()
