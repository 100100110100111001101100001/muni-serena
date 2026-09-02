from django.urls import path
from . import views

app_name = 'gestion_territorial'

urlpatterns = [
    path('', views.vista_inicio, name='inicio'),
    # TODO (compañero): agregar la ruta de la ficha personal, ej:
    # path('funcionario/<int:id_funcionario>/', views.vista_ficha_personal, name='ficha'),
]
