from django.shortcuts import render


def resumen_general(request):
	delegaciones = [
		{
			'nombre': 'Las Compañías',
			'atenciones_diarias': '38',
			'actividades_cumplidas': '7',
			'cumplimiento_diario': '86%',
			'avance_meta': '78%',
			'dias_restantes': '18',
		},
		{
			'nombre': 'La Pampa',
			'atenciones_diarias': '24',
			'actividades_cumplidas': '5',
			'cumplimiento_diario': '82%',
			'avance_meta': '74%',
			'dias_restantes': '18',
		},
		{
			'nombre': 'La Antena - La Florida',
			'atenciones_diarias': '31',
			'actividades_cumplidas': '6',
			'cumplimiento_diario': '89%',
			'avance_meta': '81%',
			'dias_restantes': '18',
		},
		{
			'nombre': 'Avenida del Mar',
			'atenciones_diarias': '19',
			'actividades_cumplidas': '4',
			'cumplimiento_diario': '76%',
			'avance_meta': '68%',
			'dias_restantes': '18',
		},
		{
			'nombre': 'Centro',
			'atenciones_diarias': '46',
			'actividades_cumplidas': '9',
			'cumplimiento_diario': '93%',
			'avance_meta': '88%',
			'dias_restantes': '18',
		},
		{
			'nombre': 'Rural',
			'atenciones_diarias': '16',
			'actividades_cumplidas': '3',
			'cumplimiento_diario': '71%',
			'avance_meta': '63%',
			'dias_restantes': '18',
		},
	]
	return render(request, 'resumenAlcaldeApp/resumen.html', {
		'delegaciones': delegaciones,
		'periodo': 'Evaluación de gestión municipal 2026',
	})
