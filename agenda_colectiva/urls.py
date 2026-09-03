from django.urls import path
from . import views

# OJO: sin app_name (el nuevo blueprint usa nombres de URL planos, sin
# namespace, para poder usar {% url 'tubo_tablero' %} directo en base.html)

urlpatterns = [
    path('kanban/', views.vista_tubo_tablero, name='tubo_tablero'),
    path('kanban/crear/', views.vista_crear_compromiso, name='crear_compromiso'),
    path('kanban/mover/', views.vista_mover_compromiso, name='mover_compromiso'),

    # Extra que no esta en el blueprint nuevo, la dejamos por si sirve
    path('resumen/', views.vista_resumen_colectivo, name='resumen_colectivo'),
]
