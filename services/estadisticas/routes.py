from flask import Blueprint, render_template, request
from services.estadisticas.models import obtener_estadisticas_por_tipo_prueba, obtener_zonas,  obtener_estadisticas_nacionales

estadisticas_bp = Blueprint('estadisticas', __name__)

@estadisticas_bp.route('/estadisticas', methods=['GET'])
def mostrar_estadisticas():
    # Obtener filtro de zona desde la URL
    zona_id = request.args.get('zona_id')  # Parámetro opcional

    # Obtener las estadísticas filtradas por zona (o sin filtro si zona_id es None)
    estadisticas = obtener_estadisticas_por_tipo_prueba(zona_id=zona_id)

    # Obtener todas las zonas para el filtro
    zonas = obtener_zonas()

    # Renderizar la plantilla
    return render_template(
        'funcionarios/funcionarios_estadisticas_local.html',
        estadisticas=estadisticas,
        zonas=zonas,
        zona_seleccionada=int(zona_id) if zona_id else None  # Para marcar la zona seleccionada en el frontend
    )

@estadisticas_bp.route('/estadisticas/nacional', methods=['GET'])
def mostrar_estadisticas_nacionales():
    # Obtener las estadísticas nacionales
    estadisticas_nacionales = obtener_estadisticas_nacionales()

    # Extraer enfermedades únicas
    enfermedades = list(set([estadistica['enfermedad'] for estadistica in estadisticas_nacionales]))

    # Renderizar la plantilla para estadísticas nacionales
    return render_template(
        'funcionarios/funcionarios_estadisticas_nacional.html',
        estadisticas_nacionales=estadisticas_nacionales,
        enfermedades=enfermedades
    )
