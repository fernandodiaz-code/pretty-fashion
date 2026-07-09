from django.db import models
from vendedores.models import StaffUser


class Recarga(models.Model):
    ESTADOS = [
        ("vacio", "Vacío"),
        ("concho", "Concho"),
    ]

    LUGARES_VENTA = [
        ("local", "Local"),
        ("camion", "Camión"),
    ]

    METODOS_PAGO = [
        ("efectivo", "Efectivo"),
        ("debito", "Débito"),
        ("transferencia", "Transferencia"),
        ("credito", "Crédito"),
        ("bono_gobierno", "Bono del gobierno"),
        ("vale_fisico", "Vale físico"),
        ("vale_digital", "Vale digital"),
    ]

    TIPOS_QR = [
        ("ninguno", "Ninguno"),
        ("qr_local", "QR local"),
        ("qr_camion", "QR domicilio/camión"),
    ]

    galon_peso = models.IntegerField()
    estado_recibido = models.CharField(max_length=10, choices=ESTADOS)
    lugar_venta = models.CharField(
        max_length=10, choices=LUGARES_VENTA, default="local"
    )
    cliente_rut = models.CharField(max_length=12, blank=True, default="")
    cliente_nombre = models.CharField(max_length=100, blank=True, default="")
    vendedor = models.ForeignKey(
        StaffUser, on_delete=models.SET_NULL, blank=True, null=True
    )
    precio_base = models.IntegerField(default=0)
    descuento_total = models.IntegerField(default=0)
    aplica_qr = models.BooleanField(default=False)
    tipo_qr = models.CharField(max_length=10, choices=TIPOS_QR, default="ninguno")
    comentario = models.TextField(blank=True, default="")
    monto = models.IntegerField()
    metodo_pago = models.CharField(
        max_length=20, choices=METODOS_PAGO, default="efectivo"
    )
    pago_mixto = models.BooleanField(default=False)
    monto_pago_1 = models.IntegerField(default=0)
    metodo_pago_2 = models.CharField(
        max_length=20, choices=METODOS_PAGO, blank=True, default=""
    )
    monto_pago_2 = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "recargas"

    def __str__(self):
        return f"Venta {self.id} - {self.galon_peso}kg"

    def resumen_pago(self):
        if self.pago_mixto:
            return (
                f"{self.get_metodo_pago_display()} ${self.monto_pago_1:,} + "
                f"{self.get_metodo_pago_2_display()} ${self.monto_pago_2:,}"
            ).replace(",", ".")
        return self.get_metodo_pago_display()
