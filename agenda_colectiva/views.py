from django.shortcuts import render, redirect
from django.contrib import messages
from .services import TuboTrabajoService
from .forms import CompromisoForm
from ficha_desempeno.services import FuncionariosService


def vista_tubo_tablero(request):
    compromisos = TuboTrabajoService.get_all()
    funcionarios = {f['id']: f['nombre'] for f in FuncionariosService.get_all()}

    # Inyectar el nombre de funcionario responsable a cada compromiso
    for c in compromisos:
        c['responsable_nombre'] = funcionarios.get(c['responsable_id'], "No Asignado")

    kanban = {
        'ingresado': [c for c in compromisos if c['estado'] == 'Ingresado'],
        'pendiente': [c for c in compromisos if c['estado'] == 'Pendiente'],
        'en_proceso': [c for c in compromisos if c['estado'] == 'En Proceso'],
        'realizado': [c for c in compromisos if c['estado'] == 'Realizado'],
    }

    # Calcular meta de cumplimiento colectiva del SGR (Minimo 80% exigido)
    totales = len(compromisos)
    realizados = len(kanban['realizado'])
    porcentaje_avance_comunal = (realizados / totales * 100) if totales > 0 else 100

    context = {
        'kanban': kanban,
        'avance_comunal': round(porcentaje_avance_comunal, 2),
        'form': CompromisoForm()
    }
    return render(request, 'agenda_colectiva/tubo_tablero.html', context)


def vista_crear_compromiso(request):
    if request.method == 'POST':
        form = CompromisoForm(request.POST)
        if form.is_valid():
            TuboTrabajoService.create(form.cleaned_data)
            messages.success(request, "Nuevo compromiso insertado exitosamente en la Agenda Colectiva.")
        else:
            messages.error(request, "Error de validación en los datos del compromiso. Por favor, revise el formulario.")
    return redirect('tubo_tablero')


def vista_editar_compromiso(request, compromiso_id):
    compromiso = TuboTrabajoService.get_by_id(compromiso_id)
    if request.method == 'POST':
        form = CompromisoForm(request.POST)
        if form.is_valid():
            TuboTrabajoService.update(compromiso_id, form.cleaned_data)
            messages.success(request, f"Compromiso {compromiso_id} actualizado con éxito.")
            return redirect('tubo_tablero')
    else:
        form = CompromisoForm(initial={
            'vecino': compromiso['vecino'],
            'telefono': compromiso['telefono'],
            'territorio': compromiso['territorio'],
            'descripcion': compromiso['descripcion'],
            'fecha_compromiso': compromiso['fecha_compromiso'],
            'responsable_id': compromiso['responsable_id']
        })
    return render(request, 'agenda_colectiva/editar_compromiso.html', {'form': form, 'compromiso_id': compromiso_id})


def vista_eliminar_compromiso(request, compromiso_id):
    TuboTrabajoService.delete(compromiso_id)
    messages.warning(request, f"El compromiso {compromiso_id} ha sido borrado físicamente del JSON.")
    return redirect('tubo_tablero')


def vista_cambiar_estado(request, compromiso_id):
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        TuboTrabajoService.update_estado(compromiso_id, nuevo_estado)
        messages.success(request, f"Estado del compromiso {compromiso_id} actualizado a {nuevo_estado}.")
    return redirect('tubo_tablero')
