from django.urls import path
from . import views

urlpatterns = [
    path("consulta/", views.consultar_cliente, name="consultar_cliente"),
]
