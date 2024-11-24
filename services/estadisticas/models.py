from db_connection import get_db_connection

def obtener_estadisticas_por_tipo_prueba(zona_id=None):
    """
    Consulta SQL para obtener estadísticas por tipo de prueba, opcionalmente filtradas por zona.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT 
            tp.prueba AS tipo_prueba,
            COUNT(CASE WHEN r.resultado = 'positivo' THEN 1 END) AS total_positivos,
            COUNT(CASE WHEN r.resultado = 'negativo' THEN 1 END) AS total_negativos,
            COUNT(r.resultado) AS total
        FROM 
            cliente c
        JOIN 
            cliente_cita cc ON c.id_cliente = cc.cliente_id_cliente
        JOIN 
            prueba p ON cc.id_cliente_cita = p.cliente_cita_id_cliente_cita
        JOIN 
            resutlado r ON p.id_prueba = r.prueba_id_prueba
        JOIN 
            tipo_prueba tp ON p.tipo_prueba_id_tipo_prueba = tp.id_tipo_prueba
        JOIN 
            zona z ON c.zona_id_zona = z.id_zona
    """

    # Añadir filtro de zona si se proporciona
    params = []
    if zona_id:
        query += " WHERE z.id_zona = %s"
        params.append(zona_id)

    query += " GROUP BY tp.prueba ORDER BY tp.prueba"

    # Ejecutar la consulta
    cursor.execute(query, params)
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultados


def obtener_zonas():
    """
    Consulta SQL para obtener todas las zonas disponibles.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = "SELECT id_zona, zona FROM zona ORDER BY id_zona"
    cursor.execute(query)
    zonas = cursor.fetchall()  # Devuelve una lista de diccionarios [{'id_zona': 1, 'zona': 'Zona Norte'}, ...]
    cursor.close()
    conn.close()
    return zonas


def obtener_estadisticas_nacionales():
    """
    Consulta SQL para obtener estadísticas nacionales consolidadas por región y enfermedad.
    """
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT 
            z.zona AS region,
            tp.prueba AS enfermedad,
            COUNT(CASE WHEN r.resultado = 'positivo' THEN 1 END) AS total_positivos,
            COUNT(CASE WHEN r.resultado = 'negativo' THEN 1 END) AS total_negativos,
            COUNT(r.resultado) AS total_pruebas
        FROM 
            cliente c
        JOIN 
            cliente_cita cc ON c.id_cliente = cc.cliente_id_cliente
        JOIN 
            prueba p ON cc.id_cliente_cita = p.cliente_cita_id_cliente_cita
        JOIN 
            resutlado r ON p.id_prueba = r.prueba_id_prueba
        JOIN 
            tipo_prueba tp ON p.tipo_prueba_id_tipo_prueba = tp.id_tipo_prueba
        JOIN 
            zona z ON c.zona_id_zona = z.id_zona
        GROUP BY 
            z.zona, tp.prueba
        ORDER BY 
            z.zona, tp.prueba
    """

    cursor.execute(query)
    resultados = cursor.fetchall()
    cursor.close()
    conn.close()
    return resultados
