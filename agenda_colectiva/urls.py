from django.urls import path
from . import views

urlpatterns = [
    path('kanban/', views.vista_tubo_tablero, name='tubo_tablero'),
    path('kanban/crear/', views.vista_crear_compromiso, name='crear_compromiso'),
    path('kanban/editar/<int:compromiso_id>/', views.vista_editar_compromiso, name='editar_compromiso'),
    path('kanban/eliminar/<int:compromiso_id>/', views.vista_eliminar_compromiso, name='eliminar_compromiso'),
    path('kanban/estado/<int:compromiso_id>/', views.vista_cambiar_estado, name='cambiar_estado'),
]
