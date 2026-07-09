from dataclasses import dataclass

from django.db import transaction

from inventario.models import Galon
from .models import Recarga


QR_LOCAL_FIJO = {5: 2500, 11: 4000, 15: 5500}
METODOS_VALE = ("vale_fisico", "vale_digital")
PESOS_VALIDOS = (5, 11, 15, 45)


class VentaValidationError(ValueError):
    pass


@dataclass
class VentaRegistrada:
    recarga: Recarga
    galon: Galon


def parse_entero(valor, default=0):
    try:
        return int(valor)
    except (TypeError, ValueError):
        return default


def calcular_descuento(lugar_venta, peso, aplica_qr, descuento_manual):
    """Calcula el descuento_total en base a las reglas de negocio."""
    if not aplica_qr:
        return 0

    if lugar_venta == "local" and peso in QR_LOCAL_FIJO:
        return QR_LOCAL_FIJO[peso]

    return max(descuento_manual, 0)


def registrar_venta(datos):
    peso = parse_entero(datos.get("peso"), 0)
    estado = datos.get("estado") or datos.get("estado_recibido") or "vacio"
    lugar_venta = datos.get("lugar_venta") or "local"
    metodo_pago = datos.get("metodo_pago") or "efectivo"
    pago_mixto = datos.get("pago_mixto") in (True, "true", "True", "1", "on", 1)
    metodo_pago_2 = datos.get("metodo_pago_2") or ""
    monto_pago_1 = parse_entero(datos.get("monto_pago_1"), 0)
    monto_pago_2 = parse_entero(datos.get("monto_pago_2"), 0)
    aplica_qr = datos.get("aplica_qr") in (True, "true", "True", "1", "on", 1)
    descuento_manual = parse_entero(datos.get("descuento_manual"), 0)
    comentario = (datos.get("comentario") or "").strip()
    vendedor = datos.get("vendedor")

    if lugar_venta not in ("local", "camion"):
        raise VentaValidationError("Lugar de venta no válido.")

    if estado not in ("vacio", "concho"):
        raise VentaValidationError("Estado recibido no válido.")

    metodos_validos = [codigo for codigo, _ in Recarga.METODOS_PAGO]
    if metodo_pago not in metodos_validos:
        raise VentaValidationError("Método de pago no válido.")

    if pago_mixto and metodo_pago_2 not in metodos_validos:
        raise VentaValidationError("Segundo método de pago no válido.")

    if peso not in PESOS_VALIDOS:
        raise VentaValidationError("Peso de galón no válido.")

    with transaction.atomic():
        try:
            galon = Galon.objects.select_for_update().get(peso=peso)
        except Galon.DoesNotExist as exc:
            raise VentaValidationError(
                f"No hay configuración para galones de {peso}kg."
            ) from exc

        if galon.llenos <= 0:
            raise VentaValidationError(
                f"No hay galones llenos de {peso}kg disponibles."
            )

        precio_base = galon.precio
        descuento_total = calcular_descuento(
            lugar_venta, peso, aplica_qr, descuento_manual
        )

        if descuento_total < 0 or descuento_total > precio_base:
            raise VentaValidationError(
                "El descuento no puede ser negativo ni mayor al precio base."
            )

        monto = precio_base - descuento_total
        if metodo_pago in METODOS_VALE:
            monto = 0

        if pago_mixto:
            if monto == 0:
                raise VentaValidationError(
                    "No se puede usar pago mixto cuando el total final es $0."
                )

            if metodo_pago in METODOS_VALE or metodo_pago_2 in METODOS_VALE:
                raise VentaValidationError(
                    "Los vales deben registrarse como método de pago único."
                )

            if metodo_pago == metodo_pago_2:
                raise VentaValidationError(
                    "Seleccione dos métodos de pago distintos para pago mixto."
                )

            if monto_pago_1 <= 0 or monto_pago_2 <= 0:
                raise VentaValidationError(
                    "Los montos del pago mixto deben ser mayores a $0."
                )

            if monto_pago_1 + monto_pago_2 != monto:
                raise VentaValidationError(
                    "La suma del pago mixto debe ser igual al total final."
                )
        else:
            metodo_pago_2 = ""
            monto_pago_1 = monto
            monto_pago_2 = 0

        tipo_qr = "ninguno"
        if aplica_qr:
            tipo_qr = "qr_local" if lugar_venta == "local" else "qr_camion"

        if lugar_venta != "camion":
            comentario = ""

        galon.llenos -= 1
        if estado == "vacio":
            galon.vacios += 1
        else:
            galon.conchos += 1
        galon.save()

        recarga = Recarga.objects.create(
            galon_peso=peso,
            estado_recibido=estado,
            lugar_venta=lugar_venta,
            vendedor=vendedor,
            precio_base=precio_base,
            descuento_total=descuento_total,
            aplica_qr=aplica_qr,
            tipo_qr=tipo_qr,
            comentario=comentario,
            monto=monto,
            metodo_pago=metodo_pago,
            pago_mixto=pago_mixto,
            monto_pago_1=monto_pago_1,
            metodo_pago_2=metodo_pago_2,
            monto_pago_2=monto_pago_2,
        )

    return VentaRegistrada(recarga=recarga, galon=galon)

