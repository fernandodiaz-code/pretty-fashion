
from django.db import models

class Vendedor(models.Model):
    nombre = models.CharField(max_length=100)
    rut = models.CharField(max_length=12, unique=True)
    correo = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.rut})"
