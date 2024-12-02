from flask import Flask, render_template
from services.client.routes import client_bp
from services.operador.routes import operator_bp
from services.funcionario.routes import funcionario_bp
from services.doctor.routes import doctor_bp
from services.admin.routes import admin_bp
from services.auth.routes import auth_bp

app = Flask(__name__)
app.secret_key = 'clave_secreta'

app.register_blueprint(client_bp, url_prefix='/client')
app.register_blueprint(operator_bp, url_prefix='/operator')
app.register_blueprint(funcionario_bp, url_prefix='/funcionario')
app.register_blueprint(doctor_bp, url_prefix='/doctor')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(auth_bp, url_prefix='/auth')

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)
