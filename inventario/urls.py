from django.urls import path
from . import views

urlpatterns = [
    path("menu/", views.menu_inventario, name="menu_inventario"),
    path("consulta/", views.consultar_inventario, name="consultar_inventario"),  # <- corregido
    path("consultar_por_codigo/", views.consultar_por_codigo, name="consultar_por_codigo"),
    path("ingresar/", views.ingresar_stock, name="ingresar_stock"),
    path("consultar_por_tipo/", views.consultar_por_tipo, name="consultar_por_tipo"),
]