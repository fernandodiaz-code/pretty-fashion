"""
URL configuration for pretty_fashion project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include 
from ventas import views  
from inventario import views 
from clientes import views
from vendedores import views
from jefatura import views 
from informes import views 
urlpatterns = [
    path('admin/', admin.site.urls),
   path('ventas/', include('ventas.urls')), 
path('inventario/', include('inventario.urls')),
path('clientes/', include('clientes.urls')),
path('vendedores/', include('vendedores.urls')),
path('jefatura/', include('jefatura.urls')),
path('informes/', include('informes.urls')),

 
]
