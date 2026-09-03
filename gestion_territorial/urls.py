from django.urls import path
from . import views

# Sin app_name: el blueprint nuevo usa nombres de URL planos (ver base.html)

urlpatterns = [
    path('', views.vista_inicio, name='inicio'),
    path('ficha/<int:funcionario_id>/', views.vista_ficha_personal, name='ficha_personal'),
]
