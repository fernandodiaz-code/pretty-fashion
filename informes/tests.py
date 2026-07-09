from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from io import BytesIO
from zipfile import ZipFile

from ventas.models import Recarga


class ReporteFinalDiaTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username="admin",
            password="adminpass",
            is_staff=True,
        )
        self.venta = Recarga.objects.create(
            galon_peso=11,
            estado_recibido="vacio",
            lugar_venta="local",
            precio_base=22000,
            descuento_total=4000,
            monto=18000,
            metodo_pago="efectivo",
        )

    def test_reporte_final_dia_muestra_ventas_de_hoy(self):
        self.client.login(username="admin", password="adminpass")

        response = self.client.get(reverse("reporte_final_dia"))

        self.assertContains(response, "Reporte Final Día")
        self.assertContains(response, "11 kg")
        self.assertContains(response, "18000")

    def test_descarga_reporte_final_dia_en_xlsx(self):
        self.client.login(username="admin", password="adminpass")

        response = self.client.get(reverse("descargar_reporte_final_dia"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response["Content-Type"],
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        self.assertIn(".xlsx", response["Content-Disposition"])
        with ZipFile(BytesIO(response.content)) as archivo:
            self.assertIn("xl/worksheets/sheet1.xml", archivo.namelist())
            contenido = archivo.read("xl/worksheets/sheet1.xml").decode("utf-8")
        self.assertIn("Metodo de pago", contenido)
        self.assertIn("11 kg", contenido)
        self.assertIn("18000", contenido)
