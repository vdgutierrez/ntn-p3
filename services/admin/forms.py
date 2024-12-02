from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class RegisterPersonaForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    apellido = StringField('Apellido', validators=[DataRequired(), Length(max=100)])
    correo = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    telefono = StringField('Teléfono', validators=[Length(max=11)])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar Contraseña', validators=[DataRequired(), EqualTo('password')])
    zona = SelectField('Zona', coerce=int, validators=[DataRequired()])
    tipo_persona = SelectField('Tipo de Personal', choices=[
        ('funcionario', 'Funcionario'),
        ('medico', 'Médico'),
        ('operador', 'Operador')
    ], validators=[DataRequired()])
    consultorio = SelectField('Consultorio', coerce=int)
    submit = SubmitField('Registrar')
