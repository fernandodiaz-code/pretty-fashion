from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


def root_redirect(request):
    if not request.user.is_authenticated:
        return redirect('/login/')
    if request.user.is_staff:
        return redirect('/jefatura/')
    return redirect('/ventas/venta/')


urlpatterns = [
    path('', login_required(root_redirect, login_url='/login/'), name='root'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    path('api/', include('ventas.api_urls')),
    path('apiventas/', include('ventas.api_urls')),
    path('ventas/', include('ventas.urls')),
    path('inventario/', include('inventario.urls')),
    path('vendedores/', include('vendedores.urls')),
    path('jefatura/', include('jefatura.urls')),
    path('informes/', include('informes.urls')),
]
