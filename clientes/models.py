from django.db import models


class Customer(models.Model):
    document_number = models.CharField(max_length=12, unique=True)
    first_name = models.CharField(max_length=100, blank=True, default="")
    last_name = models.CharField(max_length=100, blank=True, default="")
    phone = models.CharField(max_length=20, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "customers"

    def __str__(self):
        name = f"{self.first_name} {self.last_name}".strip()
        return name or self.document_number
