from django.db import models


class AjusteInventario(models.Model):
    TIPOS = [
        ("robo", "Robo"),
        ("perdida", "Pérdida"),
        ("rotura", "Rotura"),
        ("otro", "Otro"),
    ]

    galon_peso = models.IntegerField()
    tipo = models.CharField(max_length=20, choices=TIPOS)
    cantidad = models.IntegerField()
    notas = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "ajustes_inventario"

    def __str__(self):
        return f"Ajuste {self.tipo} - {self.galon_peso}kg x{self.cantidad}"
