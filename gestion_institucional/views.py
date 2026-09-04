from django.shortcuts import render


def vista_inicio(request):
    # Contexto comunal extraído de la documentación institucional
    delegaciones = [
        {"nombre": "Las Compañías", "encargado": "Pablo Cuadra Corrales", "direccion": "Esmeralda 2422", "tipo": "Urbana"},
        {"nombre": "La Pampa", "encargado": "María Soledad Rojas", "direccion": "Larraín Alcalde 3505", "tipo": "Urbana"},
        {"nombre": "La Antena - La Florida", "encargado": "Elizabeth Villanueva Oyarce", "direccion": "Avenida 18 de Septiembre S/N", "tipo": "Urbana"},
        {"nombre": "Avenida del Mar", "encargado": "Rodrigo Fuenzalida Vásquez", "direccion": "Avenida del Mar 2500", "tipo": "Costera"},
        {"nombre": "Centro", "encargado": "Manuel Barraza Delgado", "direccion": "Cienfuegos 226", "tipo": "Urbana/Patrimonial"},
        {"nombre": "Rural", "encargado": "Alan Von Kretschmann", "direccion": "O'Higgins 154", "tipo": "Rural Dispersa"}
    ]

    context = {
        'comuna': 'La Serena',
        'poblacion_total': 250141,
        'poblacion_urbana_pct': 89.14,
        'poblacion_rural_pct': 10.86,
        'delegaciones': delegaciones
    }
    return render(request, 'gestion_institucional/inicio.html', context)
