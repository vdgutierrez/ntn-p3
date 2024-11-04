from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Ruta de inicio
@app.route('/')
def index():
    return render_template('index.html')

# Rutas para autenticación de usuarios
@app.route('/login')
def login():
    return render_template('users/login.html')

@app.route('/register')
def register():
    return render_template('users/register.html')

# Rutas para el operador
@app.route('/pruebas')
def pruebas():
    return render_template('operador/pruebas.html')

@app.route('/citas')
def citas():
    return render_template('operador/citas.html')

@app.route('/resultados')
def resultados():
    return render_template('operador/resultados.html')

@app.route('/logout')
def logout():
    # Aquí podrías agregar la lógica para cerrar sesión si es necesario
    return "Sesión cerrada"

@app.route('/navbar_operador')
def navbar_operador():
    return render_template('operador/navbar_operador.html')

@app.route('/registro_tipoprueba', methods=['GET', 'POST'])
def registro_tipoprueba():
    if request.method == 'POST':
        # Lógica para manejar el formulario y guardar el tipo de prueba en la base de datos
        nombre_prueba = request.form['nombre_prueba']
        enfermedad = request.form['enfermedad']
        descripcion = request.form['descripcion']
        tipo_muestra = request.form['tipo_muestra']
        instrucciones = request.form.get('instrucciones', '')
        tiempo_entrega = request.form['tiempo_entrega']
        
        # Aquí añadirías el código para guardar esta información en tu base de datos

        # Redirige a otra página (por ejemplo, /pruebas) después de registrar
        return redirect(url_for('pruebas'))

    return render_template('operador/registro_tipoprueba.html')

# -------------------------------
@app.route('/cita_cliente')
def cita_cliente():
    return render_template('clientes/cita_cliente.html')





@app.route('/admin_registro_usuario', methods=['GET', 'POST'])
def registro_usuario():
    if request.method == 'POST':
        # Lógica para procesar y almacenar el usuario en la base de datos
        pass
    return render_template('admin/registro_usuario.html')

@app.route('/admin_estadistica_locales')
def ver_estadisticas_locales():
    # Aquí puedes traer datos de la base de datos para mostrar en la vista
    return render_template('admin/estadistica_locales.html')


# Rutas para los funcionarios
@app.route('/funcionarios_estadisticas_local')
def funcionarios_estadisticas_local():
    return render_template('funcionarios/funcionarios_estadisticas_local.html')

@app.route('/funcionarios_estadisticas_nacional')
def funcionarios_estadisticas_nacional():
    return render_template('funcionarios/funcionarios_estadisticas_nacional.html')

@app.route('/funcionarios_comunicacion', methods=['GET', 'POST'])
def funcionarios_comunicacion():
    if request.method == 'POST':
        cliente_info = request.form['cliente_info']
        # Aquí podrías realizar la búsqueda del cliente en la base de datos usando `cliente_info`
        # Luego puedes pasar los datos del cliente a la plantilla
        return render_template('funcionarios/funcionarios_comunicacion.html', cliente_info=cliente_info)

    return render_template('funcionarios/funcionarios_comunicacion.html')

if __name__ == '__main__':
    app.run(debug=True)
