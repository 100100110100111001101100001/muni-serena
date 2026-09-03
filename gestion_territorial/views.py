from django.shortcuts import render

# TODO (compañero): crear gestion_territorial/services.py con la clase
# FuncionariosAPI (get_all_funcionarios / get_funcionario_by_id) que lea
# funcionarios.json, y usarla aca en vez de los datos de ejemplo de abajo.
# Ver blueprint-final-muni-serena.md seccion 5 para el codigo completo.

def vista_inicio(request):
    context = {
        'funcionarios': [],
        'habitantes': '250.141',
        'urbanos_pct': '89.14%',
        'rurales_pct': '10.86%',
    }
    return render(request, 'gestion_territorial/inicio.html', context)


def vista_ficha_personal(request, funcionario_id):
    # TODO (compañero): reemplazar por FuncionariosAPI.get_funcionario_by_id
    # y la logica real del semaforo diario (ver blueprint-final seccion 5.D).
    context = {
        'funcionario': {'id': funcionario_id, 'nombre': 'Pendiente de implementar', 'cargo': '', 'delegacion': '', 'items': []},
        'cumplimiento': 0,
        'meta_esperada_hoy': 0,
        'color_semaforo': 'secondary',
        'label_semaforo': 'Pendiente de implementar',
        'dias_transcurridos': 0,
        'dias_totales': 0,
    }
    return render(request, 'gestion_territorial/ficha_personal.html', context)
