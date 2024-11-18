from flask import Blueprint, render_template

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/registro_usuario', methods=['GET', 'POST'])
def registro_usuario():
    if request.method == 'POST':
        # Lógica para registrar un usuario
        pass
    return render_template('admin/registro_usuario.html')

@admin_bp.route('/estadistica_locales')
def estadistica_locales():
    return render_template('admin/estadistica_locales.html')
