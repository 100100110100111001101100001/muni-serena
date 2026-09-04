from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gestion_institucional.urls')),   # App 1 (Estudiante 2)
    path('desempeno/', include('ficha_desempeno.urls')),  # App 2 (Estudiante 2)
    path('agenda/', include('agenda_colectiva.urls')),     # App 3 (Estudiante 1)
    path('social/', include('atencion_social.urls')),      # App 4 (Estudiante 1)
]
