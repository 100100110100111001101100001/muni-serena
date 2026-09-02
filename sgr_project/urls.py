from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('gestion_territorial.urls')),       # App 1 (compañero)
    path('agenda/', include('agenda_colectiva.urls')),    # App 2 (yo)
]
