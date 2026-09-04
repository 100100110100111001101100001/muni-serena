from django.urls import path
from . import views

urlpatterns = [
    path('personal/', views.vista_ficha_personal_lista, name='ficha_personal_lista'),
    path('personal/<int:funcionario_id>/', views.vista_ficha_personal, name='ficha_personal_detalle'),
    path('personal/<int:funcionario_id>/registrar/', views.vista_registrar_actividad, name='registrar_actividad'),
]
