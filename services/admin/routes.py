from flask import Blueprint, render_template, flash, redirect, url_for, request
from db_connection import get_db_connection
from .forms import RegisterPersonaForm

admin_bp = Blueprint('admin', __name__, template_folder='templates')

@admin_bp.route('/register_persona', methods=['GET', 'POST'])
def register_persona():
    form = RegisterPersonaForm()
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    # Cargar zonas y consultorios dinámicamente
    cursor.execute("SELECT id_zona, zona FROM zona")
    form.zona.choices = [(z['id_zona'], z['zona']) for z in cursor.fetchall()]
    
    cursor.execute("SELECT id_consultorio, consultorio FROM consultorio")
    form.consultorio.choices = [(c['id_consultorio'], c['consultorio']) for c in cursor.fetchall()]
    
    if form.validate_on_submit():
        tipo_persona = form.tipo_persona.data
        nombre = form.nombre.data
        apellido = form.apellido.data
        correo = form.correo.data
        telefono = form.telefono.data if tipo_persona in ['medico', 'operador'] else None
        password = form.password.data
        zona = form.zona.data
        consultorio = form.consultorio.data if tipo_persona in ['medico', 'operador'] else None
        
        table_map = {
            'funcionario': 'funcionario',
            'medico': 'medico',
            'operador': 'operador'
        }
        table_name = table_map[tipo_persona]
        
        try:
            query = f"""
                INSERT INTO {table_name} (nombre, apellido, correo, contrasena, zona_id_zona{', telefono, consultorio_id_consultorio' if tipo_persona in ['medico', 'operador'] else ''})
                VALUES (%s, %s, %s, %s, %s{', %s, %s' if tipo_persona in ['medico', 'operador'] else ''})
            """
            params = [nombre, apellido, correo, password, zona]
            if tipo_persona in ['medico', 'operador']:
                params.extend([telefono, consultorio])
            
            cursor.execute(query, params)
            connection.commit()
            flash(f'{tipo_persona.capitalize()} registrado con éxito.', 'success')
            return redirect(url_for('admin.register_persona'))
        except Exception as e:
            connection.rollback()
            flash(f'Error al registrar: {e}', 'danger')
        finally:
            cursor.close()
            connection.close()
    
    return render_template('register_persona.html', form=form)
