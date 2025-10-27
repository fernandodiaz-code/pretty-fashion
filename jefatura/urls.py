from django.urls import path
from . import views

urlpatterns = [
    path('', views.menu_jefatura, name='menu_jefatura'),
    path('nota_credito/', views.nota_credito, name='nota_credito'),
    path('vendedores/', views.gestion_vendedores_admin, name='gestion_vendedores_admin'),
    path('vendedores/agregar/', views.agregar_vendedor, name='agregar_vendedor'),
    path('modificar_inventario_robo/', views.modificar_inventario_robo, name='modificar_inventario_robo'),
    path('gestion_general_sistema/', views.gestion_general_sistema, name='gestion_general_sistema'),
    path('agregar_vendedor/', views.agregar_vendedor, name='agregar_vendedor'),
    path('gestion_vendedores_admin/', views.gestion_vendedores_admin, name='gestion_vendedores_admin'),
]






