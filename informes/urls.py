from django.urls import path
from . import views

urlpatterns = [
    path("menu/", views.menu_informes, name="menu_informes"),
    path("ventas/", views.informe_recargas, name="informe_ventas"),
    path("recargas/", views.informe_recargas, name="informe_recargas"),
    path("final-dia/", views.reporte_final_dia, name="reporte_final_dia"),
    path("final-dia/descargar/", views.descargar_reporte_final_dia, name="descargar_reporte_final_dia"),
]
