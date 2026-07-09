from django.db import models


class Galon(models.Model):
    PESOS = [
        (5, '5 kg'),
        (11, '11 kg'),
        (15, '15 kg'),
        (45, '45 kg'),
    ]

    peso = models.IntegerField(choices=PESOS, unique=True)
    llenos = models.IntegerField(default=0)
    vacios = models.IntegerField(default=0)
    conchos = models.IntegerField(default=0)
    precio = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "galones"

    def __str__(self):
        return f"{self.peso}kg"


class PedidoCentral(models.Model):
    fecha = models.DateField(auto_now_add=True)
    cantidad_pedida_llenos = models.IntegerField()
    cantidad_devuelta_vacios = models.IntegerField()
    notas = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "pedidos_central"

    def __str__(self):
        return f"Pedido {self.id} - {self.fecha}"
