from django.shortcuts import render, redirect
from django.contrib import messages
from pretty_fashion.decorators import admin_required
from .models import StaffUser
from ventas.models import Recarga
from datetime import datetime


@admin_required
def menu_vendedores(request):
    vendedores = StaffUser.objects.filter(is_active=True)
    return render(request, "vendedores/menu.html", {"vendedores": vendedores})


@admin_required
def lista_vendedores(request):
    vendedores = StaffUser.objects.all()
    return render(request, "vendedores/lista.html", {"vendedores": vendedores})


@admin_required
def recargas_por_vendedor(request):
    vendedores = StaffUser.objects.filter(is_active=True)
    recargas = []
    id_vendedor = None
    nombre_vendedor = ""
    fecha_inicio = ""
    fecha_fin = ""
    total = 0

    if request.method == "POST":
        id_vendedor = request.POST.get("id_vendedor")
        fecha_inicio = request.POST.get("fecha_inicio", "")
        fecha_fin = request.POST.get("fecha_fin", "")

        try:
            vendedor = StaffUser.objects.get(id=id_vendedor)
            nombre_vendedor = str(vendedor)
            qs = Recarga.objects.filter(vendedor=vendedor)

            if fecha_inicio:
                fecha_i = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
                qs = qs.filter(created_at__date__gte=fecha_i)
            if fecha_fin:
                fecha_f = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
                qs = qs.filter(created_at__date__lte=fecha_f)

            recargas = qs.order_by("-created_at")
            total = sum(r.monto for r in recargas)
        except (StaffUser.DoesNotExist, ValueError):
            messages.error(request, "Datos inválidos.")

    return render(request, "vendedores/recargas.html", {
        "vendedores": vendedores,
        "recargas": recargas,
        "id_vendedor": id_vendedor,
        "nombre_vendedor": nombre_vendedor,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "total": total,
    })
