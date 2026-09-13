from django.urls import path

from . import views


urlpatterns = [
	path('', views.resumen_general, name='resumen_general'),
]
