from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gestion_territorial.urls')),        # App del compañero (a migrar a gestion_institucional)
    path('agenda/', include('agenda_colectiva.urls')),     # App mia (Estudiante 1)
    path('social/', include('atencion_social.urls')),      # App mia (Estudiante 1)
    # TODO (compañero): agregar aca cuando construyas tu parte:
    # path('desempeno/', include('ficha_desempeno.urls')),
]
