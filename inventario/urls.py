from django.urls import path
from . import views

urlpatterns = [
    path("menu/", views.menu_inventario, name="menu_inventario"),
    path("ajustar/<int:peso>/", views.ajustar_stock, name="ajustar_stock"),
    path("pedidos/", views.historial_pedidos, name="historial_pedidos"),
    path("pedidos/nuevo/", views.realizar_pedido, name="realizar_pedido"),
    path("pedidos/confirmar/", views.confirmar_pedido, name="confirmar_pedido"),
]
