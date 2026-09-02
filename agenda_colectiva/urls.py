from django.urls import path
from . import views

app_name = 'agenda_colectiva'

urlpatterns = [
    path('tablero/', views.vista_tubo_tablero, name='tablero'),
    path('resumen/', views.vista_resumen_colectivo, name='resumen'),
]
