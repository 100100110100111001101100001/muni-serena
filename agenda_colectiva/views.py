from django.shortcuts import render
from .services import TuboTrabajoAPI


def vista_tubo_tablero(request):
    """Carga los compromisos del JSON y los agrupa en columnas Kanban"""
    compromisos = TuboTrabajoAPI.get_all()

    kanban = {
        'ingresado': [c for c in compromisos if c['estado'] == 'Ingresado'],
        'pendiente': [c for c in compromisos if c['estado'] == 'Pendiente'],
        'en_proceso': [c for c in compromisos if c['estado'] == 'En Proceso'],
        'realizado': [c for c in compromisos if c['estado'] == 'Realizado'],
    }
    return render(request, 'agenda_colectiva/tubo_tablero.html', {'kanban': kanban})


def vista_resumen_colectivo(request):
    """Calcula los indicadores de cumplimiento colectivo de la delegacion"""
    compromisos = TuboTrabajoAPI.get_all()

    total = len(compromisos)
    realizados = len([c for c in compromisos if c['estado'] == 'Realizado'])
    pendientes = total - realizados

    # Umbral minimo exigido: 80% de compromisos cerrados
    pct_realizado = (realizados / total * 100) if total > 0 else 0
    alerta_incumplimiento = pct_realizado < 80.0

    context = {
        'compromisos': compromisos,
        'total': total,
        'realizados': realizados,
        'pendientes': pendientes,
        'porcentaje': round(pct_realizado, 2),
        'alert': alerta_incumplimiento,
    }
    return render(request, 'agenda_colectiva/resumen_colectivo.html', context)
