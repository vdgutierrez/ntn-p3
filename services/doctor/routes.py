from flask import Blueprint, render_template, session, flash, redirect, url_for, request
from db_connection import get_db_connection

doctor_bp = Blueprint('doctor', __name__, template_folder='templates')

@doctor_bp.route('/historial', methods=['GET', 'POST'])
def historial():
    # Verificar si el usuario está logueado y es médico
    if 'user' not in session or session['user']['tipo'] != 'medico':
        flash("Debes iniciar sesión como médico para acceder a esta página.", "warning")
        return redirect(url_for('auth.login'))
    
    correo_cliente = None
    historial_data = []

    if request.method == 'POST':
        # Obtener correo del formulario
        correo_cliente = request.form.get('correo_cliente')
        if not correo_cliente:
            flash("Debe ingresar un correo electrónico válido.", "warning")
            return redirect(url_for('doctor.historial'))

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            # Consulta para obtener el historial del cliente
            query = """
            SELECT cc.fecha_hora AS fecha_cita, p.descripcion AS prueba, tp.prueba AS tipo_prueba, cc.id_cliente_cita
            FROM cliente_cita cc
            INNER JOIN prueba p ON cc.id_cliente_cita = p.cliente_cita_id_cliente_cita
            INNER JOIN tipo_prueba tp ON p.tipo_prueba_id_tipo_prueba = tp.id_tipo_prueba
            INNER JOIN cliente c ON cc.cliente_id_cliente = c.id_cliente
            WHERE c.correo = %s AND cc.historial = 1
            """
            cursor.execute(query, (correo_cliente,))
            historial_data = cursor.fetchall()

            if not historial_data:
                flash("No se encontraron registros en el historial para este cliente.", "info")

        except Exception as e:
            flash(f"Error al obtener el historial: {e}", "danger")

        finally:
            cursor.close()
            connection.close()

    return render_template('historial.html', historial=historial_data, correo_cliente=correo_cliente)
