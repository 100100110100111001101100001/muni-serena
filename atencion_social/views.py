from django.shortcuts import render, redirect
from django.contrib import messages
from .services import CasosSocialesService
from .forms import CasoSocialForm, AtencionSecuencialForm


def vista_lista_casos(request):
    casos = CasosSocialesService.get_all()
    form_caso = CasoSocialForm()
    return render(request, 'atencion_social/lista_casos.html', {'casos': casos, 'form': form_caso})


def vista_crear_caso(request):
    if request.method == 'POST':
        form = CasoSocialForm(request.POST)
        if form.is_valid():
            CasosSocialesService.create_caso(form.cleaned_data)
            messages.success(request, "Beneficiario registrado con éxito en el sistema de Caso Social.")
        else:
            messages.error(request, "Errores de validación en la creación del beneficiario.")
    return redirect('lista_casos')


def vista_detalle_caso(request, caso_id):
    caso = CasosSocialesService.get_by_id(caso_id)
    limite_alcanzado = len(caso['atenciones']) >= 3

    context = {
        'caso': caso,
        'limite_alcanzado': limite_alcanzado,
        'form_atencion': AtencionSecuencialForm()
    }
    return render(request, 'atencion_social/detalle_caso.html', context)


def vista_agregar_atencion(request, caso_id):
    if request.method == 'POST':
        form = AtencionSecuencialForm(request.POST)
        if form.is_valid():
            try:
                CasosSocialesService.add_atencion(caso_id, form.cleaned_data)
                messages.success(request, "Gestión social secuencial guardada con éxito en el historial.")
            except ValueError as e:
                messages.error(request, str(e))
        else:
            messages.error(request, "Error de validación al agregar atención.")
    return redirect('detalle_caso', caso_id=caso_id)


def vista_eliminar_caso(request, caso_id):
    CasosSocialesService.delete_caso(caso_id)
    messages.warning(request, f"Caso social ID {caso_id} removido del registro comunal.")
    return redirect('lista_casos')
