from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from pretty_fashion.decorators import admin_required
from .models import Galon, PedidoCentral


@admin_required
def menu_inventario(request):
    galones = Galon.objects.all().order_by('peso')
    total_llenos = sum(g.llenos for g in galones)
    total_vacios = sum(g.vacios for g in galones)
    total_conchos = sum(g.conchos for g in galones)
    return render(request, "inventario/menu.html", {
        "galones": galones,
        "total_llenos": total_llenos,
        "total_vacios": total_vacios,
        "total_conchos": total_conchos,
    })


@admin_required
def ajustar_stock(request, peso):
    galon = get_object_or_404(Galon, peso=peso)
    if request.method == "POST":
        llenos = int(request.POST.get("llenos", 0))
        vacios = int(request.POST.get("vacios", 0))
        conchos = int(request.POST.get("conchos", 0))
        precio = request.POST.get("precio")

        galon.llenos = max(0, galon.llenos + llenos)
        galon.vacios = max(0, galon.vacios + vacios)
        galon.conchos = max(0, galon.conchos + conchos)

        if precio:
            galon.precio = int(precio)

        galon.save()
        messages.success(request, f"Stock de {peso}kg actualizado correctamente.")
        return redirect("menu_inventario")

    return render(request, "inventario/ajustar.html", {"galon": galon})


@admin_required
def historial_pedidos(request):
    pedidos = PedidoCentral.objects.all().order_by("-fecha")
    return render(request, "inventario/pedidos.html", {"pedidos": pedidos})


@admin_required
def realizar_pedido(request):
    if request.method == "POST":
        cantidad_pedida = int(request.POST.get("cantidad_pedida", 0))
        cantidad_devuelta = int(request.POST.get("cantidad_devuelta", 0))
        notas = request.POST.get("notas", "")

        if cantidad_pedida <= 0:
            messages.error(request, "Debe pedir al menos 1 galón lleno.")
            return redirect("realizar_pedido")

        PedidoCentral.objects.create(
            cantidad_pedida_llenos=cantidad_pedida,
            cantidad_devuelta_vacios=cantidad_devuelta,
            notas=notas,
        )

        messages.success(
            request,
            f"Pedido realizado: +{cantidad_pedida} llenos, -{cantidad_devuelta} vacíos."
        )
        return redirect("historial_pedidos")

    galones = Galon.objects.all().order_by('peso')
    total_vacios = sum(g.vacios for g in galones)
    return render(request, "inventario/realizar_pedido.html", {
        "galones": galones,
        "total_vacios": total_vacios,
    })


@admin_required
def confirmar_pedido(request):
    if request.method == "POST":
        pedido_id = request.POST.get("pedido_id")
        peso = int(request.POST.get("peso"))
        cantidad_llenar = int(request.POST.get("cantidad_llenar", 0))

        if cantidad_llenar <= 0:
            messages.error(request, "Cantidad inválida.")
            return redirect("historial_pedidos")

        try:
            galon = Galon.objects.get(peso=peso)
        except Galon.DoesNotExist:
            messages.error(request, f"No existe galón de {peso}kg.")
            return redirect("historial_pedidos")

        if cantidad_llenar > galon.vacios:
            messages.error(
                request,
                f"Solo hay {galon.vacios} galones vacíos de {peso}kg."
            )
            return redirect("historial_pedidos")

        galon.llenos += cantidad_llenar
        galon.vacios -= cantidad_llenar
        galon.save()

        messages.success(
            request,
            f"{cantidad_llenar} galones de {peso}kg marcados como llenos."
        )
        return redirect("menu_inventario")

    return redirect("menu_inventario")
