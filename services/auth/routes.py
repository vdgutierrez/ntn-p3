from flask import Blueprint, request, redirect, url_for, session, render_template, flash
from db_connection import get_db_connection
from services.auth.forms import LoginForm, RegisterForm

auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        correo = form.email.data
        password = form.password.data

        connection = get_db_connection()
        try:
            cursor = connection.cursor(dictionary=True)

            # Tablas de usuarios y sus rutas de redirección
            user_tables = {
                'funcionario': 'funcionario.estadisticas',
                'operador': 'operator.resultados',
                'medico': 'doctor.historial',
                'cliente': 'client.cliente_op',
                'admin': 'admin.register_persona'
            }

            # Verificar en cada tabla si el usuario existe
            for table_name, redirect_route in user_tables.items():
                query = f"SELECT correo, contrasena, nombre FROM {table_name} WHERE correo = %s"
                cursor.execute(query, (correo,))
                user = cursor.fetchone()

                if user:  # Verificar si se encontró un usuario
                    if user['contrasena'] == password:
                        session['user'] = {
                            'correo': user['correo'],
                            'nombre': user['nombre'],  # Cambia según el nombre exacto de la columna en la base de datos
                            'tipo': table_name
                        }
                        session['logged_in'] = True
                        flash('Inicio de sesión exitoso', 'success')
                        return redirect(url_for(redirect_route))
                    else:
                        flash('Contraseña incorrecta', 'danger')
                        break
            else:
                flash('Correo no encontrado', 'danger')
        finally:
            connection.close()

    return render_template('login.html', form=form)


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión exitosamente', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    
    # Conexión a la base de datos para obtener zonas
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT id_zona, zona FROM zona")
    zonas = cursor.fetchall()
    
    # Calcular el próximo ID de cliente
    cursor.execute("SELECT MAX(id_cliente) AS max_id FROM cliente")
    result = cursor.fetchone()
    next_id = result['max_id'] + 1 if result['max_id'] else 1  # Si no hay registros, iniciar en 1
    connection.close()
    
    # Convertir zonas en opciones para el SelectField
    form.zona.choices = [(zona['id_zona'], zona['zona']) for zona in zonas]
    
    if request.method == 'POST' and form.validate_on_submit():
        # Recoger los datos del formulario
        nombre = form.nombre.data
        apellido = form.apellido.data
        fecha_nacimiento = form.fecha_nacimiento.data
        genero = form.genero.data  # Este valor ya será "Masculino" o "Femenino"
        correo = form.correo.data
        telefono = form.telefono.data
        zona_id_zona = form.zona.data
        password = form.password.data
        
        # Guardar el cliente en la base de datos
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            query = """
                INSERT INTO cliente (id_cliente, nombre, apellido, fecha_nacimiento, genero, correo, contrasena, telefono, zona_id_zona)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (next_id, nombre, apellido, fecha_nacimiento, genero, correo, password, telefono, zona_id_zona))
            connection.commit()
            flash('Registro exitoso. Por favor, inicie sesión.', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            connection.rollback()
            flash(f'Error al registrar: {e}', 'danger')
        finally:
            cursor.close()
            connection.close()

    return render_template('register.html', form=form)
