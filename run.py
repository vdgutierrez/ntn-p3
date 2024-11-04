from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Ruta de inicio
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('users/login.html')

@app.route('/register')
def register():
    return render_template('users/register.html')

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

if __name__ == '__main__':
    app.run(debug=True)
