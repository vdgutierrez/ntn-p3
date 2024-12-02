from flask import Blueprint, render_template, session, flash, redirect, url_for
from db_connection import get_db_connection

client_bp = Blueprint('client', __name__, template_folder='templates')

@client_bp.route('/cliente_op')
def cliente_op():
    # Verificar si el cliente está logueado
    if 'user' not in session:
        flash("Debes iniciar sesión para acceder a esta página.", "warning")
        return redirect(url_for('auth.login'))
    
    # Renderizar la vista de opciones del cliente
    return render_template('cliente_op.html')

@client_bp.route('/cita', methods=['GET', 'POST'])
def cita():
    # Verificar si el cliente está logueado
    if 'user' not in session:
        flash("Debes iniciar sesión para programar una cita.", "warning")
        return redirect(url_for('auth.login'))

    # Conexión a la base de datos
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    operadores = []
    tipos_prueba = []

    try:
        # Obtener la zona del cliente logueado
        cursor.execute("SELECT zona_id_zona FROM cliente WHERE correo = %s", (session['user']['correo'],))
        cliente_data = cursor.fetchone()

        if not cliente_data:
            flash("No se encontró información de zona para el cliente logueado.", "danger")
        else:
            zona_cliente = cliente_data['zona_id_zona']

            # Obtener operadores de la misma zona
            cursor.execute("""
                SELECT nombre, apellido 
                FROM operador 
                WHERE zona_id_zona = %s
            """, (zona_cliente,))
            operadores = cursor.fetchall()

            if not operadores:
                flash("No se encontraron operadores en tu zona.", "info")

        # Obtener los tipos de prueba disponibles
        cursor.execute("SELECT prueba FROM tipo_prueba")
        tipos_prueba = cursor.fetchall()

        if not tipos_prueba:
            flash("No hay tipos de prueba disponibles.", "info")

    except Exception as e:
        flash(f"Error al obtener datos: {e}", "danger")

    finally:
        cursor.close()
        connection.close()

    # Renderizar plantilla con datos dinámicos
    return render_template(
        'cita.html',
        operadores=operadores,
        tipos_prueba=tipos_prueba
    )

@client_bp.route('/resultado', methods=['GET'])
def resultado():
    # Verificar si el cliente está logueado
    if 'user' not in session:
        flash("Debes iniciar sesión para acceder a esta página.", "warning")
        return redirect(url_for('auth.login'))
    
    # Renderizar la plantilla de resultados
    return render_template('resultado.html')
