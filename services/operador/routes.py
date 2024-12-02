from flask import Blueprint, render_template

operator_bp = Blueprint('operator', __name__, template_folder='templates')

@operator_bp.route('/operador_op')
def operador_op():
    return render_template('operador_op.html')