from django.shortcuts import render


def dashboard_evidencias(request):
	evidencias = [
		{
			'id': 1,
			'titulo': 'Mejoramiento de áreas verdes',
			'responsable': 'Dirección de Medio Ambiente',
			'fecha': '12 de septiembre de 2026',
			'imagen': 'img/evidenciasApp/parque1.jpg',
		},
		{
			'id': 2,
			'titulo': 'Actividad comunitaria Mallplaza',
			'responsable': 'Delegación Centro',
			'fecha': '10 de septiembre de 2026',
			'imagen': 'img/evidenciasApp/Mallplaza.jpg',
		},
		{
			'id': 3,
			'titulo': 'Coordinación con compañías locales',
			'responsable': 'Secretaría Comunal de Planificación',
			'fecha': '8 de septiembre de 2026',
			'imagen': 'img/evidenciasApp/companias.jpg',
		},
	]
	return render(request, 'evidenciasApp/dashboard.html', {'evidencias': evidencias})
