from django.urls import path
from . import views

urlpatterns = [
    path('casos/', views.vista_lista_casos, name='lista_casos'),
    path('casos/crear/', views.vista_crear_caso, name='crear_caso'),
    path('casos/<int:caso_id>/', views.vista_detalle_caso, name='detalle_caso'),
    path('casos/<int:caso_id>/atencion/', views.vista_agregar_atencion, name='agregar_atencion'),
    path('casos/<int:caso_id>/eliminar/', views.vista_eliminar_caso, name='eliminar_caso'),
]
