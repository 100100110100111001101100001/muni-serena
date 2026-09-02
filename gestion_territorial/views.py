from django.shortcuts import render

# TODO (compañero): crear gestion_territorial/services.py con la clase
# FuncionariosAPI (get_all / get_by_id) que lea funcionarios.json, y usarla
# aca en vez de la lista vacia de abajo.

def vista_inicio(request):
    context = {
        'funcionarios': [],
        'habitantes': '250.141',
        'urbanos_pct': '89.14%',
        'rurales_pct': '10.86%',
    }
    return render(request, 'gestion_territorial/inicio.html', context)

# TODO (compañero): vista_ficha_personal con la logica del semaforo diario
