from django.urls import path

from . import views


urlpatterns = [
	path('', views.periodos_lista, name='periodos_lista'),
	path('crear/', views.crear_periodo, name='crear_periodo'),
	path('editar/<int:periodo_id>/', views.editar_periodo, name='editar_periodo'),
	path('eliminar/<int:periodo_id>/', views.eliminar_periodo, name='eliminar_periodo'),
]
