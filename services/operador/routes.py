from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from db_connection import get_db_connection
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart

# Blueprint para el módulo operador
operator_bp = Blueprint('operator', __name__, template_folder='templates')

@operator_bp.route('/resultados', methods=['GET', 'POST'])
def resultados():
    # Verificar si el usuario ha iniciado sesión
    if 'user' not in session:
        flash("Debes iniciar sesión para acceder a esta página.", "warning")
        return redirect(url_for('auth.login'))

    # Manejar el método GET (mostrar el formulario)
    if request.method == 'GET':
        # Obtener tipos de prueba para el formulario
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            query = "SELECT id_tipo_prueba, prueba FROM tipo_prueba"
            cursor.execute(query)
            tipos_prueba = cursor.fetchall()
        except Exception as e:
            flash(f"Error al obtener tipos de prueba: {e}", "danger")
            tipos_prueba = []
        finally:
            cursor.close()
            connection.close()

        return render_template('resultados.html', tipos_prueba=tipos_prueba)

    # Manejar el método POST (procesar y enviar resultados)
    if request.method == 'POST':
        cliente_id = request.form.get('cliente_id')
        tipo_prueba_id = request.form.get('tipo_prueba')
        resultado = request.form.get('resultado')
        
        # Validar datos básicos
        if not cliente_id or not tipo_prueba_id or not resultado:
            flash("Todos los campos son obligatorios.", "danger")
            return redirect(url_for('operator.enviar_resultados'))

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            # Verificar que el cliente exista
            cursor.execute("SELECT correo, nombre FROM cliente WHERE id_cliente = %s", (cliente_id,))
            cliente = cursor.fetchone()
            if not cliente:
                flash("El cliente con el ID proporcionado no existe.", "danger")
                return redirect(url_for('operator.enviar_resultados'))

            # Insertar el resultado en la base de datos
            query_resultado = """
                INSERT INTO resutlado (resultado, fecha, prueba_id_prueba, detalle)
                VALUES (%s, CURDATE(), %s, %s)
            """
            prueba_id = tipo_prueba_id  # Supongamos que hay una relación directa entre tipo y prueba
            cursor.execute(query_resultado, (resultado, prueba_id, resultado))
            connection.commit()

            # Enviar el correo al cliente
            #enviar_correo(cliente['correo'], cliente['nombre'], resultado)

            flash("Resultados enviados exitosamente al cliente.", "success")
            return redirect(url_for('operator.resultados'))
        except Exception as e:
            connection.rollback()
            flash(f"Error al enviar resultados: {e}", "danger")
        finally:
            cursor.close()
            connection.close()

    return redirect(url_for('operator.enviar_resultados'))


# def enviar_correo(destinatario, nombre_cliente, resultado):
#     # Configuración del servidor SMTP
#     servidor_smtp = "smtp.gmail.com"
#     puerto_smtp = 587
#     correo_emisor = "ignacio.agramont.11@gmail.com"  
#     contrasena = "tu_contrasena"  

#     # Crear el mensaje del correo
#     mensaje = MIMEMultipart()
#     mensaje['From'] = correo_emisor
#     mensaje['To'] = destinatario
#     mensaje['Subject'] = "Resultados de tu prueba"

#     cuerpo = f"""
#     Hola {nombre_cliente},

#     Los resultados de tu prueba están disponibles. Aquí está el detalle:

#     {resultado}

#     Saludos,
#     Equipo Médico
#     """
#     mensaje.attach(MIMEText(cuerpo, 'plain'))

#     try:
#         # Conectar al servidor SMTP y enviar el correo
#         servidor = smtplib.SMTP(servidor_smtp, puerto_smtp)
#         servidor.starttls()
#         servidor.login(correo_emisor, contrasena)
#         servidor.send_message(mensaje)
#         servidor.quit()
#         print("Correo enviado exitosamente")
#     except Exception as e:
#         print(f"Error al enviar correo: {e}")

@operator_bp.route('/citas', methods=['GET'])
def citas():
    # Verificar si el usuario ha iniciado sesión
    if 'user' not in session:
        flash("Debes iniciar sesión para acceder a esta página.", "warning")
        return redirect(url_for('auth.login'))

    # Conexión a la base de datos
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        # Obtener todas las citas programadas con información relevante
        query = """
        SELECT 
            cc.id_cliente_cita AS id_cita,
            c.id_cliente AS id_cliente,
            CONCAT(c.nombre, ' ', c.apellido) AS nombre_cliente,
            cc.fecha_hora AS fecha_hora,
            tp.prueba AS tipo_prueba,
            CASE 
                WHEN cc.historial = 1 THEN 'Completada'
                ELSE 'Pendiente'
            END AS estado
        FROM cliente_cita cc
        INNER JOIN cliente c ON cc.cliente_id_cliente = c.id_cliente
        INNER JOIN prueba p ON cc.id_cliente_cita = p.cliente_cita_id_cliente_cita
        INNER JOIN tipo_prueba tp ON p.tipo_prueba_id_tipo_prueba = tp.id_tipo_prueba
        ORDER BY cc.fecha_hora;
        """
        cursor.execute(query)
        citas_programadas = cursor.fetchall()

    except Exception as e:
        flash(f"Error al obtener citas: {e}", "danger")
        citas_programadas = []

    finally:
        cursor.close()
        connection.close()

    # Renderizar la plantilla con las citas
    return render_template('citas.html', citas=citas_programadas)

@operator_bp.route('/registro_tipo', methods=['GET', 'POST'])
def registro_tipo():
    if 'user' not in session:
        flash("Debes iniciar sesión para acceder a esta página.", "warning")
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        # Obtener datos del formulario
        nombre_prueba = request.form.get('nombre_prueba')
        enfermedad = request.form.get('enfermedad')
        descripcion = request.form.get('descripcion')
        tipo_muestra = request.form.get('tipo_muestra')
        instrucciones = request.form.get('instrucciones', None)  # Campo opcional
        tiempo_entrega = request.form.get('tiempo_entrega')

        # Validación de campos obligatorios
        if not nombre_prueba or not enfermedad or not descripcion or not tipo_muestra or not tiempo_entrega:
            flash('Por favor, completa todos los campos obligatorios.', 'danger')
            return redirect(url_for('operator.registro_tipo'))

        # Conexión a la base de datos
        connection = get_db_connection()
        cursor = connection.cursor()

        try:
            # Verificar si la enfermedad ya existe en la base de datos
            cursor.execute("SELECT id_enfermedad FROM enfermedad WHERE enfermnedad = %s", (enfermedad,))
            enfermedad_row = cursor.fetchone()

            if not enfermedad_row:
                # Si la enfermedad no existe, agregarla
                cursor.execute(
                    "INSERT INTO enfermedad (enfermnedad, descripcion) VALUES (%s, %s)",
                    (enfermedad, f"Detectado por {nombre_prueba}"),
                )
                connection.commit()
                enfermedad_id = cursor.lastrowid
            else:
                enfermedad_id = enfermedad_row[0]

            # Insertar el nuevo tipo de prueba en la base de datos
            cursor.execute(
                """
                INSERT INTO tipo_prueba (prueba, descripcion, enfermedad_id_enfermedad)
                VALUES (%s, %s, %s)
                """,
                (nombre_prueba, descripcion, enfermedad_id),
            )
            connection.commit()

            flash('Tipo de prueba registrado exitosamente.', 'success')
            return redirect(url_for('operator.registro_tipo'))

        except Exception as e:
            connection.rollback()
            flash(f"Error al registrar el tipo de prueba: {e}", 'danger')
        finally:
            cursor.close()
            connection.close()

    return render_template('registro_tipoprueba.html')

@operator_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    # Verificar si el usuario ha iniciado sesión
    if 'user' not in session:
        flash("Debes iniciar sesión para acceder a esta página.", "warning")
        return redirect(url_for('auth.login'))

    if request.method == 'GET':
        # Obtener los tipos de prueba desde la base de datos
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            query = "SELECT id_tipo_prueba, prueba FROM tipo_prueba"
            cursor.execute(query)
            tipos_prueba = cursor.fetchall()  # Lista de diccionarios
        except Exception as e:
            flash(f"Error al obtener tipos de prueba: {e}", "danger")
            tipos_prueba = []  # Asegúrate de asignar una lista vacía en caso de error
        finally:
            cursor.close()
            connection.close()

        # Renderizar el formulario con los tipos de prueba
        return render_template('pruebas.html', tipos_prueba=tipos_prueba)

    if request.method == 'POST':
        cliente_id = request.form.get('cliente_id')
        tipo_prueba_id = request.form.get('tipo_prueba')
        observaciones = request.form.get('observaciones', '')

        # Validar datos básicos
        if not cliente_id or not tipo_prueba_id:
            flash("El ID del cliente y el tipo de prueba son obligatorios.", "danger")
            return redirect(url_for('operator.registro'))

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            # Verificar que el cliente exista
            cursor.execute("SELECT id_cliente FROM cliente WHERE id_cliente = %s", (cliente_id,))
            cliente = cursor.fetchone()
            if not cliente:
                flash("El cliente con el ID proporcionado no existe.", "danger")
                return redirect(url_for('operator.registro'))

            # Registrar la prueba
            query_prueba = """
                INSERT INTO prueba (descripcion, cliente_cita_id_cliente_cita, tipo_prueba_id_tipo_prueba, medico_id_cmedico)
                VALUES (%s, %s, %s, %s)
            """
            descripcion = observaciones or "Sin observaciones"
            cliente_cita_id = cliente_id  # Confirma que esta relación es correcta en tu modelo
            medico_id = 1  # Lógica para determinar el médico
            cursor.execute(query_prueba, (descripcion, cliente_cita_id, tipo_prueba_id, medico_id))
            connection.commit()

            flash("Prueba registrada exitosamente.", "success")
            return redirect(url_for('operator.resultados'))
        except Exception as e:
            connection.rollback()
            flash(f"Error al registrar la prueba: {e}", "danger")
        finally:
            cursor.close()
            connection.close()

    # Solo se llega aquí en caso de error, redirige de nuevo
    return redirect(url_for('operator.registro'))