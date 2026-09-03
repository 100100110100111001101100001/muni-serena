import datetime

from django.http import Http404
from django.shortcuts import render

from .services import FuncionariosAPI


def _rango_trimestre_actual(hoy=None):
    """Devuelve la fecha de inicio y fin del trimestre calendario en curso"""
    hoy = hoy or datetime.date.today()
    trimestre = (hoy.month - 1) // 3 + 1
    mes_inicio = (trimestre - 1) * 3 + 1
    inicio = datetime.date(hoy.year, mes_inicio, 1)
    if trimestre == 4:
        fin = datetime.date(hoy.year, 12, 31)
    else:
        fin = datetime.date(hoy.year, mes_inicio + 3, 1) - datetime.timedelta(days=1)
    return inicio, fin


def _dias_habiles(inicio, fin):
    """Cuenta los dias laborales (lun a vie) entre dos fechas, inclusive"""
    total = 0
    dia = inicio
    while dia <= fin:
        if dia.weekday() < 5:
            total += 1
        dia += datetime.timedelta(days=1)
    return total


def _calcular_semaforo(funcionario):
    """Calcula la meta esperada al dia, el cumplimiento real y el color del semaforo"""
    inicio, fin = _rango_trimestre_actual()
    dias_totales = _dias_habiles(inicio, fin)
    hoy = datetime.date.today()
    dias_transcurridos = _dias_habiles(inicio, hoy) if hoy <= fin else dias_totales

    meta_esperada_hoy = round((dias_transcurridos / dias_totales) * 100, 2) if dias_totales else 0
    meta_trimestre = funcionario.get('meta_trimestre') or 0
    avance_actual = funcionario.get('avance_actual') or 0
    cumplimiento = round((avance_actual / meta_trimestre) * 100, 2) if meta_trimestre else 0

    if cumplimiento >= meta_esperada_hoy:
        color, texto = 'success', 'Cumplimiento al día'
    elif cumplimiento >= meta_esperada_hoy * 0.60:
        color, texto = 'warning', 'Cumplimiento en riesgo'
    else:
        color, texto = 'danger', 'Cumplimiento atrasado'

    return {
        'dias_totales': dias_totales,
        'dias_transcurridos': dias_transcurridos,
        'meta_esperada_hoy': meta_esperada_hoy,
        'cumplimiento': cumplimiento,
        'color_semaforo': color,
        'texto_semaforo': texto,
    }


def vista_inicio(request):
    """Lista los funcionarios del JSON en tarjetas con su avance trimestral"""
    funcionarios = FuncionariosAPI.get_all()
    for f in funcionarios:
        meta = f.get('meta_trimestre') or 0
        avance = f.get('avance_actual') or 0
        f['pct_avance'] = round((avance / meta) * 100, 1) if meta else 0

    delegaciones = sorted({f.get('delegacion') for f in funcionarios if f.get('delegacion')})

    context = {
        'funcionarios': funcionarios,
        'delegaciones': delegaciones,
        'habitantes': '250.141',
        'urbanos_pct': '89.14%',
        'rurales_pct': '10.86%',
    }
    return render(request, 'gestion_territorial/inicio.html', context)


def vista_ficha_personal(request, id_funcionario):
    """Ficha de desempeno del funcionario con la logica del semaforo diario"""
    funcionario = FuncionariosAPI.get_by_id(id_funcionario)
    if funcionario is None:
        raise Http404('Funcionario no encontrado')

    context = {'funcionario': funcionario}
    context.update(_calcular_semaforo(funcionario))
    return render(request, 'gestion_territorial/ficha_personal.html', context)
