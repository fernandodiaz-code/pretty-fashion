from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from inventario.models import Galon


class GestionPreciosTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username="admin",
            password="adminpass",
            is_staff=True,
        )
        self.galon_5 = Galon.objects.create(peso=5, llenos=3, precio=12000)
        self.galon_11 = Galon.objects.create(peso=11, llenos=2, precio=21000)

    def test_admin_actualiza_precios_de_gas(self):
        self.client.login(username="admin", password="adminpass")

        response = self.client.post(reverse("gestionar_precios"), {
            f"precio_{self.galon_5.id}": "13000",
            f"precio_{self.galon_11.id}": "22000",
        })

        self.assertRedirects(response, reverse("gestionar_precios"))
        self.galon_5.refresh_from_db()
        self.galon_11.refresh_from_db()
        self.assertEqual(self.galon_5.precio, 13000)
        self.assertEqual(self.galon_11.precio, 22000)

    def test_realizar_venta_muestra_precio_actualizado(self):
        self.galon_5.precio = 13500
        self.galon_5.save()
        self.client.login(username="admin", password="adminpass")

        response = self.client.get(reverse("realizar_venta"))

        self.assertContains(response, 'data-precio="13500"')
