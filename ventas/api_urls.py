from django.urls import path

from . import api_views


urlpatterns = [
    path("ventas/config/", api_views.ventas_config, name="api_ventas_config"),
    path("ventas/", api_views.registrar_venta_api, name="api_registrar_venta"),
]

