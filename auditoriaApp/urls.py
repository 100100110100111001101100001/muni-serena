from django.urls import path

from . import views


urlpatterns = [
	path('', views.registros_auditoria, name='registros_auditoria'),
]
