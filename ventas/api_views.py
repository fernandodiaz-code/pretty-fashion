import json

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from inventario.models import Galon
from .models import Recarga
from .services import QR_LOCAL_FIJO, VentaValidationError, registrar_venta


def _recarga_payload(recarga):
    return {
        "id": recarga.id,
        "galon_peso": recarga.galon_peso,
        "estado_recibido": recarga.estado_recibido,
        "lugar_venta": recarga.lugar_venta,
        "precio_base": recarga.precio_base,
        "descuento_total": recarga.descuento_total,
        "aplica_qr": recarga.aplica_qr,
        "tipo_qr": recarga.tipo_qr,
        "comentario": recarga.comentario,
        "monto": recarga.monto,
        "metodo_pago": recarga.metodo_pago,
        "pago_mixto": recarga.pago_mixto,
        "monto_pago_1": recarga.monto_pago_1,
        "metodo_pago_2": recarga.metodo_pago_2,
        "monto_pago_2": recarga.monto_pago_2,
        "created_at": timezone.localtime(recarga.created_at).isoformat(),
    }


@require_GET
@login_required
def ventas_config(request):
    galones = Galon.objects.all().order_by("peso")
    return JsonResponse({
        "galones": [
            {
                "peso": galon.peso,
                "label": f"{galon.peso} kg",
                "llenos": galon.llenos,
                "vacios": galon.vacios,
                "conchos": galon.conchos,
                "precio": galon.precio,
            }
            for galon in galones
        ],
        "estados_recibidos": [
            {"codigo": codigo, "nombre": nombre}
            for codigo, nombre in Recarga.ESTADOS
        ],
        "lugares_venta": [
            {"codigo": codigo, "nombre": nombre}
            for codigo, nombre in Recarga.LUGARES_VENTA
        ],
        "metodos_pago": [
            {"codigo": codigo, "nombre": nombre}
            for codigo, nombre in Recarga.METODOS_PAGO
        ],
        "qr_local_fijo": QR_LOCAL_FIJO,
    })


@csrf_exempt
@require_POST
@login_required
def registrar_venta_api(request):
    try:
        datos = json.loads(request.body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        return JsonResponse({
            "ok": False,
            "error": "JSON inválido.",
        }, status=400)

    try:
        venta = registrar_venta(datos)
    except VentaValidationError as exc:
        return JsonResponse({
            "ok": False,
            "error": str(exc),
        }, status=400)

    return JsonResponse({
        "ok": True,
        "venta": _recarga_payload(venta.recarga),
        "stock": {
            "peso": venta.galon.peso,
            "llenos": venta.galon.llenos,
            "vacios": venta.galon.vacios,
            "conchos": venta.galon.conchos,
        },
    }, status=201)

