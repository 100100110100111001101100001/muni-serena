from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .services import TuboTrabajoAPI


def vista_tubo_tablero(request):
    compromisos = TuboTrabajoAPI.get_all_compromisos()

    # Clasificacion por columna Kanban estilo Jira/Scrum
    kanban = {
        'ingresado': [c for c in compromisos if c['estado'] == 'Ingresado'],
        'pendiente': [c for c in compromisos if c['estado'] == 'Pendiente'],
        'en_proceso': [c for c in compromisos if c['estado'] == 'En Proceso'],
        'realizado': [c for c in compromisos if c['estado'] == 'Realizado'],
    }

    # Lista estatica para asignaciones en el modal de creacion
    funcionarios_disponibles = ["María Fonseca Palma", "Alberto Barrientos"]

    # Calculo grupal de cumplimiento (meta minima exigida: 80%)
    totales = len(compromisos)
    realizados = len(kanban['realizado'])
    porcentaje_avance_colectivo = (realizados / totales * 100) if totales > 0 else 0

    context = {
        'kanban': kanban,
        'funcionarios': funcionarios_disponibles,
        'cumplimiento_grupal': round(porcentaje_avance_colectivo, 1),
    }
    return render(request, 'agenda_colectiva/tubo_tablero.html', context)


@require_POST
def vista_crear_compromiso(request):
    solicitante = request.POST.get('vecino_solicitante')
    telefono = request.POST.get('telefono')
    territorio = request.POST.get('territorio')
    descripcion = request.POST.get('descripcion')
    fecha = request.POST.get('fecha_compromiso')
    responsable = request.POST.get('responsable_nombre')

    TuboTrabajoAPI.create_compromiso(solicitante, telefono, territorio, descripcion, fecha, responsable)
    return redirect('tubo_tablero')


@require_POST
def vista_mover_compromiso(request):
    id_comp = request.POST.get('id_compromiso')
    nuevo_estado = request.POST.get('nuevo_estado')

    TuboTrabajoAPI.update_estado_compromiso(id_comp, nuevo_estado)
    return redirect('tubo_tablero')


def vista_resumen_colectivo(request):
    """Ruta extra que no esta en el blueprint nuevo, se deja disponible igual"""
    compromisos = TuboTrabajoAPI.get_all_compromisos()

    total = len(compromisos)
    realizados = len([c for c in compromisos if c['estado'] == 'Realizado'])
    pendientes = total - realizados
    pct_realizado = (realizados / total * 100) if total > 0 else 0

    context = {
        'compromisos': compromisos,
        'total': total,
        'realizados': realizados,
        'pendientes': pendientes,
        'porcentaje': round(pct_realizado, 2),
        'alert': pct_realizado < 80.0,
    }
    return render(request, 'agenda_colectiva/resumen_colectivo.html', context)
