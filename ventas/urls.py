from django.urls import path
from . import views

urlpatterns = [
    path("venta/", views.realizar_recarga, name="realizar_venta"),
    path("recarga/", views.realizar_recarga, name="realizar_recarga"),
    path("calcular_precio/", views.calcular_precio_ajax, name="calcular_precio_ajax"),
]
