from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from inventario.models import Galon
from .models import Recarga


class RealizarVentaTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="vendedor",
            password="testpass",
        )
        Galon.objects.create(peso=11, llenos=2, precio=22000)

    def test_vales_guardan_total_final_cero(self):
        self.client.login(username="vendedor", password="testpass")

        for metodo_pago in ("vale_fisico", "vale_digital"):
            with self.subTest(metodo_pago=metodo_pago):
                response = self.client.post(reverse("realizar_venta"), {
                    "peso": "11",
                    "estado": "vacio",
                    "lugar_venta": "local",
                    "metodo_pago": metodo_pago,
                })

                self.assertEqual(response.status_code, 200)
                venta = Recarga.objects.latest("id")
                self.assertEqual(venta.precio_base, 22000)
                self.assertEqual(venta.monto, 0)
                self.assertContains(response, "&#36;0", html=False)

    def test_pago_mixto_guarda_dos_metodos_si_suma_total(self):
        self.client.login(username="vendedor", password="testpass")

        response = self.client.post(reverse("realizar_venta"), {
            "peso": "11",
            "estado": "vacio",
            "lugar_venta": "local",
            "metodo_pago": "debito",
            "pago_mixto": "on",
            "monto_pago_1": "12000",
            "metodo_pago_2": "efectivo",
            "monto_pago_2": "10000",
        })

        self.assertEqual(response.status_code, 200)
        venta = Recarga.objects.get()
        self.assertTrue(venta.pago_mixto)
        self.assertEqual(venta.metodo_pago, "debito")
        self.assertEqual(venta.monto_pago_1, 12000)
        self.assertEqual(venta.metodo_pago_2, "efectivo")
        self.assertEqual(venta.monto_pago_2, 10000)
        self.assertEqual(venta.monto, 22000)

    def test_pago_mixto_rechaza_suma_distinta_al_total(self):
        self.client.login(username="vendedor", password="testpass")

        response = self.client.post(reverse("realizar_venta"), {
            "peso": "11",
            "estado": "vacio",
            "lugar_venta": "local",
            "metodo_pago": "debito",
            "pago_mixto": "on",
            "monto_pago_1": "12000",
            "metodo_pago_2": "efectivo",
            "monto_pago_2": "9000",
        })

        self.assertRedirects(response, reverse("realizar_venta"))
        self.assertEqual(Recarga.objects.count(), 0)


class VentasApiTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="vendedor_api",
            password="testpass",
        )
        Galon.objects.create(peso=11, llenos=2, vacios=1, conchos=0, precio=22000)

    def test_config_entrega_precios_y_stock_actuales(self):
        self.client.login(username="vendedor_api", password="testpass")

        response = self.client.get(reverse("api_ventas_config"))

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["galones"][0]["peso"], 11)
        self.assertEqual(data["galones"][0]["precio"], 22000)
        self.assertEqual(data["galones"][0]["llenos"], 2)
        self.assertIn({"codigo": "efectivo", "nombre": "Efectivo"}, data["metodos_pago"])

    def test_api_registra_venta_y_actualiza_stock(self):
        self.client.login(username="vendedor_api", password="testpass")

        response = self.client.post(
            reverse("api_registrar_venta"),
            data={
                "peso": 11,
                "estado_recibido": "vacio",
                "lugar_venta": "local",
                "metodo_pago": "efectivo",
                "aplica_qr": False,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertTrue(data["ok"])
        self.assertEqual(data["venta"]["monto"], 22000)
        self.assertEqual(Recarga.objects.count(), 1)

        galon = Galon.objects.get(peso=11)
        self.assertEqual(galon.llenos, 1)
        self.assertEqual(galon.vacios, 2)

    def test_api_rechaza_pago_mixto_con_suma_incorrecta(self):
        self.client.login(username="vendedor_api", password="testpass")

        response = self.client.post(
            reverse("api_registrar_venta"),
            data={
                "peso": 11,
                "estado_recibido": "vacio",
                "lugar_venta": "local",
                "metodo_pago": "debito",
                "pago_mixto": True,
                "monto_pago_1": 12000,
                "metodo_pago_2": "efectivo",
                "monto_pago_2": 9000,
            },
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(response.json()["ok"])
        self.assertEqual(Recarga.objects.count(), 0)
