from django.urls import path
from . import views

urlpatterns = [
    path("", views.menu_jefatura, name="menu_jefatura"),
    path("precios/", views.gestionar_precios, name="gestionar_precios"),
    path("vendedores/", views.gestion_vendedores, name="gestion_vendedores"),
    path("vendedores/agregar/", views.agregar_vendedor, name="agregar_vendedor"),
    path("vendedores/eliminar/<int:id>/", views.eliminar_vendedor, name="eliminar_vendedor"),
]
