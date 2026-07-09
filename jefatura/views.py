from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from vendedores.models import StaffUser
from inventario.models import Galon
from ventas.models import Recarga
from pretty_fashion.decorators import admin_required


@admin_required
def menu_jefatura(request):
    hoy = timezone.localdate()
    recargas_hoy = Recarga.objects.filter(created_at__date=hoy)
    total_hoy = sum(r.monto for r in recargas_hoy)
    cantidad_hoy = recargas_hoy.count()

    galones = Galon.objects.all().order_by('peso')
    total_llenos = sum(g.llenos for g in galones)
    total_vacios = sum(g.vacios for g in galones)

    vendedores_activos = StaffUser.objects.filter(is_active=True).count()

    return render(request, "jefatura/menu.html", {
        "total_hoy": total_hoy,
        "cantidad_hoy": cantidad_hoy,
        "total_llenos": total_llenos,
        "total_vacios": total_vacios,
        "galones": galones,
        "vendedores_activos": vendedores_activos,
    })


@admin_required
def gestion_vendedores(request):
    vendedores = StaffUser.objects.all()
    return render(request, "jefatura/gestion_vendedores.html", {
        "vendedores": vendedores,
    })


@admin_required
def gestionar_precios(request):
    galones = list(Galon.objects.all().order_by("peso"))

    if request.method == "POST":
        for galon in galones:
            precio = request.POST.get(f"precio_{galon.id}", "").strip()

            if not precio:
                messages.error(request, f"Debe ingresar precio para {galon.peso} kg.")
                return redirect("gestionar_precios")

            try:
                precio_numero = int(precio)
            except ValueError:
                messages.error(request, f"Precio inválido para {galon.peso} kg.")
                return redirect("gestionar_precios")

            if precio_numero < 0:
                messages.error(request, f"El precio de {galon.peso} kg no puede ser negativo.")
                return redirect("gestionar_precios")

            galon.precio = precio_numero

        Galon.objects.bulk_update(galones, ["precio"])
        messages.success(request, "Precios de gas actualizados correctamente.")
        return redirect("gestionar_precios")

    return render(request, "jefatura/gestionar_precios.html", {
        "galones": galones,
    })


@admin_required
def agregar_vendedor(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()

        if not all([username, first_name, last_name]):
            messages.error(request, "Todos los campos son obligatorios.")
            return redirect("agregar_vendedor")

        if StaffUser.objects.filter(username=username).exists():
            messages.error(request, f"El usuario '{username}' ya existe.")
            return redirect("agregar_vendedor")

        StaffUser.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
        )
        messages.success(request, "Vendedor agregado correctamente.")
        return redirect("gestion_vendedores")

    return render(request, "jefatura/agregar_vendedor.html")


@admin_required
def eliminar_vendedor(request, id):
    if request.method == "POST":
        try:
            vendedor = StaffUser.objects.get(id=id)
            vendedor.is_active = False
            vendedor.save()
            messages.success(request, "Vendedor desactivado correctamente.")
        except StaffUser.DoesNotExist:
            messages.error(request, "Vendedor no encontrado.")
    return redirect("gestion_vendedores")
