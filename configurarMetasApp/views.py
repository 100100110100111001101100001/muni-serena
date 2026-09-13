from django.contrib import messages
from django.forms import formset_factory
from django.http import Http404
from django.shortcuts import redirect, render

from .forms import ItemForm, PeriodoForm
from .services import PeriodosService

ItemFormSet = formset_factory(ItemForm, extra=1, can_delete=True)


def _guardar_periodo(request, periodo=None):
	periodo_form = PeriodoForm(request.POST)
	item_formset = ItemFormSet(request.POST)

	if periodo_form.is_valid() and item_formset.is_valid():
		items = [
			{
				'nombre': form.cleaned_data['nombre'],
				'meta': str(form.cleaned_data['meta']),
				'ponderacion': str(form.cleaned_data['ponderacion']),
			}
			for form in item_formset
			if form.cleaned_data and not form.cleaned_data.get('DELETE', False)
		]
		total_ponderacion = sum(float(item['ponderacion']) for item in items)
		if not items:
			messages.error(request, 'Agrega al menos un ítem al período.')
		elif total_ponderacion > 100:
			messages.error(request, 'La suma de las ponderaciones no puede superar el 100%.')
		elif periodo:
			PeriodosService.update(periodo['id'], periodo_form.cleaned_data['nombre'], items)
			messages.success(request, 'Período actualizado correctamente.')
			return redirect('periodos_lista')
		else:
			PeriodosService.create(periodo_form.cleaned_data['nombre'], items)
			messages.success(request, 'Período creado correctamente.')
			return redirect('periodos_lista')

	return render(request, 'configurarMetasApp/periodo_form.html', {
		'periodo_form': periodo_form,
		'item_formset': item_formset,
		'periodo': periodo,
	})


def periodos_lista(request):
	return render(request, 'configurarMetasApp/periodos_lista.html', {
		'periodos': PeriodosService.get_all(),
	})


def crear_periodo(request):
	if request.method == 'POST':
		return _guardar_periodo(request)
	return render(request, 'configurarMetasApp/periodo_form.html', {
		'periodo_form': PeriodoForm(),
		'item_formset': ItemFormSet(),
	})


def editar_periodo(request, periodo_id):
	periodo = PeriodosService.get_by_id(periodo_id)
	if periodo is None:
		raise Http404
	if request.method == 'POST':
		return _guardar_periodo(request, periodo)
	return render(request, 'configurarMetasApp/periodo_form.html', {
		'periodo_form': PeriodoForm(initial={'nombre': periodo['nombre']}),
		'item_formset': ItemFormSet(initial=periodo['items']),
		'periodo': periodo,
	})


def eliminar_periodo(request, periodo_id):
	if request.method == 'POST':
		PeriodosService.delete(periodo_id)
		messages.warning(request, 'El período fue eliminado.')
	return redirect('periodos_lista')
