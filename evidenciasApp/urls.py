from django.urls import path

from . import views


urlpatterns = [
	path('', views.dashboard_evidencias, name='dashboard_evidencias'),
]
