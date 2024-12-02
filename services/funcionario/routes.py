from flask import Blueprint, render_template, request, flash, redirect, url_for
from db_connection import get_db_connection

funcionario_bp = Blueprint('funcionario', __name__, template_folder='templates')

@funcionario_bp.route('/estadisticas', methods=['GET'])
def estadisticas():
    # Conexión a la base de datos
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    # Obtener zonas disponibles
    cursor.execute("SELECT id_zona, zona FROM zona")
    zonas = cursor.fetchall()

    # Filtro por zona
    zona_id = request.args.get('zona_id')
    zona_seleccionada = int(zona_id) if zona_id else None

    # Consulta de estadísticas
    query = """
        SELECT 
            tp.prueba AS tipo_prueba,
            SUM(CASE WHEN r.resultado = 'positivo' THEN 1 ELSE 0 END) AS total_positivos,
            SUM(CASE WHEN r.resultado = 'negativo' THEN 1 ELSE 0 END) AS total_negativos,
            COUNT(*) AS total
        FROM resutlado r
        INNER JOIN prueba p ON r.prueba_id_prueba = p.id_prueba
        INNER JOIN tipo_prueba tp ON p.tipo_prueba_id_tipo_prueba = tp.id_tipo_prueba
        INNER JOIN cliente_cita cc ON p.cliente_cita_id_cliente_cita = cc.id_cliente_cita
        INNER JOIN cliente c ON cc.cliente_id_cliente = c.id_cliente
        {zona_filter}
        GROUP BY tp.prueba
        ORDER BY tp.prueba
    """

    # Aplicar filtro por zona si es necesario
    zona_filter = ""
    if zona_seleccionada:
        zona_filter = "WHERE c.zona_id_zona = %s"
        cursor.execute(query.format(zona_filter=zona_filter), (zona_seleccionada,))
    else:
        cursor.execute(query.format(zona_filter=""))

    estadisticas = cursor.fetchall()

    connection.close()

    # Renderizar la plantilla
    return render_template(
        'estadisticas.html',
        zonas=zonas,
        estadisticas=estadisticas,
        zona_seleccionada=zona_seleccionada
    )

@funcionario_bp.route('/estadisticas_nacionales', methods=['GET'])
def estadisticas_nacionales():
    # Conexión y consulta
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    query = """
    SELECT 
        z.zona AS region,
        tp.prueba AS tipo_prueba,
        SUM(CASE WHEN r.resultado = 'positivo' THEN 1 ELSE 0 END) AS total_positivos,
        SUM(CASE WHEN r.resultado = 'negativo' THEN 1 ELSE 0 END) AS total_negativos,
        COUNT(*) AS total
    FROM resutlado r
    INNER JOIN prueba p ON r.prueba_id_prueba = p.id_prueba
    INNER JOIN tipo_prueba tp ON p.tipo_prueba_id_tipo_prueba = tp.id_tipo_prueba
    INNER JOIN cliente_cita cc ON p.cliente_cita_id_cliente_cita = cc.id_cliente_cita
    INNER JOIN cliente c ON cc.cliente_id_cliente = c.id_cliente
    INNER JOIN zona z ON c.zona_id_zona = z.id_zona
    GROUP BY z.zona, tp.prueba
    ORDER BY z.zona, tp.prueba;
    """
    cursor.execute(query)
    estadisticas = cursor.fetchall()

    # Obtener lista de enfermedades
    enfermedades_query = """
    SELECT enfermnedad FROM enfermedad;
    """
    cursor.execute(enfermedades_query)
    enfermedades = [row['enfermnedad'] for row in cursor.fetchall()]

    connection.close()

    # Obtener el filtro de enfermedad
    enfermedad_seleccionada = request.args.get('enfermedad', '')

    return render_template(
        'estadisticas_nacionales.html',
        estadisticas=estadisticas,
        enfermedades=enfermedades,
        enfermedad_seleccionada=enfermedad_seleccionada
    )


@funcionario_bp.route('/registrar_enfermedad', methods=['GET', 'POST'])
def registrar_enfermedad():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')

        if not nombre or not descripcion:
            # Validar que los campos no estén vacíos
            flash('Todos los campos son obligatorios.', 'danger')
            return redirect(url_for('funcionario.registrar_enfermedad'))

        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            # Obtener el próximo ID automáticamente
            cursor.execute("SELECT MAX(id_enfermedad) FROM enfermedad")
            max_id = cursor.fetchone()[0] or 0
            nuevo_id = max_id + 1

            # Insertar nueva enfermedad
            query = """
                INSERT INTO enfermedad (id_enfermedad, enfermnedad, descripcion)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (nuevo_id, nombre, descripcion))
            connection.commit()

            # Mensaje de éxito y redireccionamiento
            flash('Enfermedad registrada con éxito.', 'success')
            return redirect(url_for('funcionario.estadisticas'))
        except Exception as e:
            connection.rollback()
            flash(f'Error al registrar la enfermedad: {e}', 'danger')
            return redirect(url_for('funcionario.registrar_enfermedad'))
        finally:
            cursor.close()
            connection.close()

    # Método GET para mostrar el formulario
    return render_template('registrar_enfermedad.html')