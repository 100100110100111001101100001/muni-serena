from django.shortcuts import render, redirect
from django.contrib import messages
from .services import FuncionariosService


def _calcular_desempeno_comun(funcionario):
    # Reglas de negocio de la Matriz: 91 días hábiles en el Trimestre (Ej. Julio - Septiembre)
    dias_transcurridos = 46
    dias_totales = 91

    meta_esperada_hoy = (dias_transcurridos / dias_totales) * 100

    # Porcentaje de cumplimiento del funcionario respecto a su meta trimestre
    pct_cumplimiento = (funcionario['avance_actual'] / funcionario['meta_trimestre']) * 100

    # Algoritmo de Semáforo según reglas de negocio oficiales del documento:
    # Verde: avance >= esperado
    # Ámbar: avance >= 60% del esperado y < esperado
    # Rojo: avance < 60% del esperado
    if pct_cumplimiento >= meta_esperada_hoy:
        color = 'success'  # Verde
        color_label = 'VERDE (Cumpliendo Meta)'
    elif pct_cumplimiento >= (meta_esperada_hoy * 0.60):
        color = 'warning'  # Ámbar
        color_label = 'ÁMBAR (Alerta Desviación)'
    else:
        color = 'danger'  # Rojo
        color_label = 'ROJO (Insuficiente)'

    return {
        'cumplimiento': round(pct_cumplimiento, 2),
        'esperado_hoy': round(meta_esperada_hoy, 2),
        'color': color,
        'color_label': color_label,
        'dias_transcurridos': dias_transcurridos
    }


def vista_ficha_personal_lista(request):
    funcionarios = FuncionariosService.get_all()
    lista_procesada = []

    for f in funcionarios:
        desempeno = _calcular_desempeno_comun(f)
        f['cumplimiento'] = desempeno['cumplimiento']
        f['color'] = desempeno['color']
        lista_procesada.append(f)

    return render(request, 'ficha_desempeno/ficha_personal_lista.html', {'funcionarios': lista_procesada})


def vista_ficha_personal(request, funcionario_id):
    funcionario = FuncionariosService.get_by_id(funcionario_id)
    if funcionario is None:
        messages.error(request, "Funcionario no encontrado.")
        return redirect('ficha_personal_lista')
    desempeno = _calcular_desempeno_comun(funcionario)

    context = {
        'funcionario': funcionario,
        'cumplimiento': desempeno['cumplimiento'],
        'esperado_hoy': desempeno['esperado_hoy'],
        'color': desempeno['color'],
        'color_label': desempeno['color_label'],
        'dias_transcurridos': desempeno['dias_transcurridos']
    }
    return render(request, 'ficha_desempeno/ficha_personal.html', context)


def vista_registrar_actividad(request, funcionario_id):
    if request.method == 'POST':
        cantidad = request.POST.get('cantidad', 1)
        # Aquí se simula la generación inmutable del código verificador (RF-011)
        codigo_verificador = f"REF-{funcionario_id}-2026-{request.POST.get('tipo_item', 1)}"

        FuncionariosService.registrar_avance(funcionario_id, cantidad)
        messages.success(request, f"Actividad registrada con éxito. Evidencia inmutable generada: {codigo_verificador}")
        return redirect('ficha_personal_detalle', funcionario_id=funcionario_id)

    funcionario = FuncionariosService.get_by_id(funcionario_id)
    if funcionario is None:
        messages.error(request, "Funcionario no encontrado.")
        return redirect('ficha_personal_lista')
    return render(request, 'ficha_desempeno/registrar_actividad.html', {'funcionario': funcionario})
