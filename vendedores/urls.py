from django.urls import path
from . import views

urlpatterns = [
    path('menu/', views.menu_vendedores, name='menu_vendedores'),
    path('lista/', views.lista_vendedores, name='lista_vendedores'),
    path('boletas/', views.boletas_por_vendedor, name='boletas_vendedor'),  # sin parámetro
    path('ventas/', views.ventas_por_vendedor, name='ventas_vendedor'),     # sin parámetro
]
