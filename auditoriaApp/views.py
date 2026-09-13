from django.shortcuts import render


def registros_auditoria(request):
	registros = [
		{
			'fecha': '13/09/2026',
			'hora': '09:15:42',
			'usuario': 'maria.gonzalez',
			'evento': 'Actualización de meta',
			'identificador': 'AUD-2026-0001',
			'valor_antiguo': 'Meta: 70',
			'valor_nuevo': 'Meta: 80',
		},
		{
			'fecha': '12/09/2026',
			'hora': '16:28:07',
			'usuario': 'carlos.rojas',
			'evento': 'Creación de período de medición',
			'identificador': 'AUD-2026-0002',
			'valor_antiguo': 'Sin registro',
			'valor_nuevo': 'Evaluación de gestión municipal 2026',
		},
		{
			'fecha': '11/09/2026',
			'hora': '11:03:19',
			'usuario': 'ana.munoz',
			'evento': 'Cambio de estado de evidencia',
			'identificador': 'AUD-2026-0003',
			'valor_antiguo': 'Pendiente',
			'valor_nuevo': 'Aceptada',
		},
		{
			'fecha': '10/09/2026',
			'hora': '14:47:55',
			'usuario': 'pedro.silva',
			'evento': 'Edición de compromiso',
			'identificador': 'AUD-2026-0004',
			'valor_antiguo': 'En proceso',
			'valor_nuevo': 'Realizado',
		},
	]
	return render(request, 'auditoriaApp/registros.html', {'registros': registros})
