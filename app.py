from flask import Flask, render_template
from services.admin.routes import admin_bp
from services.users.routes import users_bp
from services.estadisticas.routes import estadisticas_bp
from db_connection import get_db_connection
from mysql.connector import Error
from flask import request, redirect, url_for


app = Flask(__name__)
app.secret_key = 'tu_clave_secreta'  # Necesaria para mensajes flash

# Registrar blueprints de los servicios
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(users_bp, url_prefix='/users')
app.register_blueprint(estadisticas_bp, url_prefix='/est')


# Ruta principal que llama a index.html
@app.route('/')
def index():
    return render_template('index.html')  # Asegúrate de que index.html esté ubicado correctamente


@app.route('/funcionarios')

@app.route('/register_cliente', methods=['POST'])
def register_cliente():
    id_cliente = request.form['id_cliente']
    nombre = request.form['nombre']
    apellido = request.form['apellido']
    fecha_nacimiento = request.form['fecha_nacimiento']
    genero = request.form['genero']
    correo_electronico = request.form['correo_electronico']
    direccion = request.form['direccion']
    telefono = request.form['telefono']
    nacionalidad = request.form['nacionalidad']
    estado_civil = request.form['estado_civil']

    connection = get_db_connection()
    if connection:
        cursor = connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO usuario (id_usuario, Nombre, Apellido, FechaNAcimiento, Genero, correo, direccion, NumeroTelefono, area_id_area, rol_id_rol)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (id_cliente, nombre, apellido, fecha_nacimiento, genero, correo_electronico, direccion, telefono, 1, 2))
            connection.commit()
            print("Cliente registrado exitosamente")
        except Error as e:
            print(f"Error al registrar el cliente: {e}")
        finally:
            cursor.close()
            connection.close()
    return redirect(url_for('register'))


if __name__ == '__main__':
    app.run(debug=True)
