from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render

from inventario.models import Galon
from .services import QR_LOCAL_FIJO, VentaValidationError, registrar_venta


@login_required
def realizar_recarga(request):
    galones = Galon.objects.all().order_by("peso")

    if request.method == "POST":
        try:
            venta = registrar_venta(request.POST)
        except VentaValidationError as exc:
            messages.error(request, str(exc))
            return redirect("realizar_venta")

        recarga = venta.recarga
        messages.success(
            request,
            f"Venta de {recarga.galon_peso}kg realizada. "
            f"Total: ${recarga.monto:,}".replace(",", ".")
        )

        return render(request, "ventas/recarga_ok.html", {
            "peso": recarga.galon_peso,
            "estado": recarga.estado_recibido,
            "lugar_venta": recarga.lugar_venta,
            "precio_base": recarga.precio_base,
            "descuento_total": recarga.descuento_total,
            "monto": recarga.monto,
            "metodo_pago": recarga.metodo_pago,
            "pago_mixto": recarga.pago_mixto,
            "metodo_pago_2": recarga.metodo_pago_2,
            "monto_pago_1": recarga.monto_pago_1,
            "monto_pago_2": recarga.monto_pago_2,
            "comentario": recarga.comentario,
        })

    return render(request, "ventas/recarga.html", {
        "galones": galones,
        "qr_local_fijo": QR_LOCAL_FIJO,
    })


@login_required
def calcular_precio_ajax(request):
    if request.method == "POST":
        peso = int(request.POST.get("peso", 0))
        try:
            galon = Galon.objects.get(peso=peso)
            return JsonResponse({
                "precio": galon.precio,
                "disponible": galon.llenos,
            })
        except Galon.DoesNotExist:
            return JsonResponse({"precio": 0, "disponible": 0})
    return JsonResponse({"error": "Método no permitido"}, status=405)
