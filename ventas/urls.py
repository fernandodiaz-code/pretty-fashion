# ventas/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('venta/', views.realizar_venta, name='venta'),
    path('calcular_total/', views.calcular_total_ajax, name='calcular_total_ajax'),
]