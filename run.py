from flask import Flask, request, jsonify
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# Configuración de la conexión a la base de datos en MySQL
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',  # Cambiar según tus credenciales
            password='password',  # Cambiar según tus credenciales
            database='ntn_prueba_plagas'
        )
        return connection
    except mysql.connector.Error as e:
        print(f"Error de conexión a la base de datos: {e}")
        return None

# Endpoint para que los clientes puedan programar una cita para una prueba
@app.route('/citas', methods=['POST'])
def crear_cita():
    data = request.json
    cliente_id = data.get('cliente_id')
    operador_id = data.get('operador_id')
    fecha_hora = data.get('fecha_hora')

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

    try:
        cursor = connection.cursor()
        query = "INSERT INTO Cita (FechaHora, Estado, Cliente_ID_Cliente, OperadorPrueba_ID_OperadorPrue) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (fecha_hora, 'pendiente', cliente_id, operador_id))
        connection.commit()
        return jsonify({"mensaje": "Cita creada exitosamente"}), 201
    except mysql.connector.Error as e:
        print(f"Error al crear cita: {e}")
        return jsonify({"error": "Error al crear cita"}), 500
    finally:
        cursor.close()
        connection.close()

# Endpoint para que los operadores de pruebas verifiquen citas y datos de los clientes
@app.route('/citas/<int:operador_id>', methods=['GET'])
def ver_citas_operador(operador_id):
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM Cita WHERE OperadorPrueba_ID_OperadorPrue = %s"
        cursor.execute(query, (operador_id,))
        citas = cursor.fetchall()
        return jsonify(citas), 200
    except mysql.connector.Error as e:
        print(f"Error al obtener citas: {e}")
        return jsonify({"error": "Error al obtener citas"}), 500
    finally:
        cursor.close()
        connection.close()

# Endpoint para que los operadores envíen los resultados de las pruebas
@app.route('/resultados', methods=['POST'])
def enviar_resultado():
    data = request.json
    prueba_id = data.get('prueba_id')
    resultado = data.get('resultado')

    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

    try:
        cursor = connection.cursor()
        query = "UPDATE Prueba SET Resultado = %s WHERE id_Prueba = %s"
        cursor.execute(query, (resultado, prueba_id))
        connection.commit()
        return jsonify({"mensaje": "Resultado actualizado exitosamente"}), 200
    except mysql.connector.Error as e:
        print(f"Error al actualizar resultado: {e}")
        return jsonify({"error": "Error al actualizar resultado"}), 500
    finally:
        cursor.close()
        connection.close()

# Endpoint para que los clientes puedan ver el resultado de su prueba
@app.route('/clientes/<int:cliente_id>/resultados', methods=['GET'])
def ver_resultado_cliente(cliente_id):
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM Prueba WHERE Cliente_ID_Cliente = %s"
        cursor.execute(query, (cliente_id,))
        resultados = cursor.fetchall()
        return jsonify(resultados), 200
    except mysql.connector.Error as e:
        print(f"Error al obtener resultados: {e}")
        return jsonify({"error": "Error al obtener resultados"}), 500
    finally:
        cursor.close()
        connection.close()

# Endpoint para que los funcionarios gubernamentales vean estadísticas de pruebas por región
@app.route('/estadisticas/regionales/<int:region_id>', methods=['GET'])
def ver_estadisticas_regionales(region_id):
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM EstadisticasLocales WHERE Region = %s"
        cursor.execute(query, (region_id,))
        estadisticas = cursor.fetchall()
        return jsonify(estadisticas), 200
    except mysql.connector.Error as e:
        print(f"Error al obtener estadísticas: {e}")
        return jsonify({"error": "Error al obtener estadísticas"}), 500
    finally:
        cursor.close()
        connection.close()

# Endpoint para que los médicos puedan ver el historial de pruebas de un cliente, si está habilitado
@app.route('/clientes/<int:cliente_id>/historial', methods=['GET'])
def ver_historial_medico(cliente_id):
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM Prueba WHERE Cliente_ID_Cliente = %s AND HistorialHabilitado = TRUE"
        cursor.execute(query, (cliente_id,))
        historial = cursor.fetchall()
        return jsonify(historial), 200
    except mysql.connector.Error as e:
        print(f"Error al obtener historial: {e}")
        return jsonify({"error": "Error al obtener historial"}), 500
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)
