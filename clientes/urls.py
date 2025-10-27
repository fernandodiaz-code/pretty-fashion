from django.urls import path
from . import views

urlpatterns = [
    path('consultar_boletas/', views.consultar_boletas_por_rut_web, name='consultar_boletas'),
]