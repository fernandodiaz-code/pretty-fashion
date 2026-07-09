from django.urls import path
from . import views

urlpatterns = [
    path("menu/", views.menu_vendedores, name="menu_vendedores"),
    path("lista/", views.lista_vendedores, name="lista_vendedores"),
    path("ventas/", views.recargas_por_vendedor, name="ventas_vendedor"),
    path("recargas/", views.recargas_por_vendedor, name="recargas_vendedor"),
]
