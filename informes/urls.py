from django.urls import path
from . import views

urlpatterns = [
    path('menu/', views.menu_informes, name='menu_informes'),
    path('ventas/', views.informe_ventas, name='informe_ventas'),
    path('notas_credito/', views.informe_notas_credito, name='informe_notas_credito'),
]

