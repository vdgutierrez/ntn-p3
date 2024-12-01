from flask import Blueprint, render_template, request, flash, redirect, url_for
from db_connection import get_db_connection, close_db_connection

users_bp = Blueprint('users', __name__)


# Ruta de login
@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        connection = get_db_connection()
        if connection:
            try:
                cursor = connection.cursor(dictionary=True)
                query = "SELECT * FROM cliente WHERE correo = %s AND contrasena = %s"
                cursor.execute(query, (email, password))
                user = cursor.fetchone()
                if user:
                    flash('Inicio de sesión exitoso.', 'success')
                    return redirect(url_for('opciones'))
                else:
                    flash('Correo o contraseña incorrectos.', 'danger')
            finally:
                close_db_connection(connection)

    return render_template('users/login.html')

@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        pass
    return render_template('users/register.html')

@users_bp.route('/dashboard')
def dashboard():
    return "<h1>Bienvenido al panel de usuario</h1>"
