# views.py (parte mejorada)
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import mysql.connector
import win32print
from datetime import date

def realizar_venta(request):
    if request.method == "POST":
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Sistemasinfo123",
                database="pretty_fashion"
            )
            cursor = conexion.cursor()

            id_vendedor = request.POST.get("id_vendedor")
            rut_cliente = request.POST.get("rut_cliente")
            codigos_barra = request.POST.get("codigos_barra", "").strip().split("\n")
            metodo_pago = request.POST.get("metodo_pago")
            numero_operacion = request.POST.get("numero_operacion")
            monto_efectivo = request.POST.get("monto_efectivo")

            if rut_cliente != "777777777":
                cursor.execute("SELECT * FROM clientes WHERE rut_cliente = %s", (rut_cliente,))
                if not cursor.fetchone():
                    nombre = request.POST.get("nombre")
                    apellido = request.POST.get("apellido")
                    cursor.execute("INSERT INTO clientes (rut_cliente, nombre, apellido) VALUES (%s, %s, %s)",
                                   (rut_cliente, nombre, apellido))
                    conexion.commit()

            total = 0
            articulos = []
            for cod in codigos_barra:
                cod = cod.strip()
                if not cod:
                    continue
                cursor.execute("SELECT id_articulo, precio, cantidad FROM articulo WHERE codigo_barra = %s", (cod,))
                result = cursor.fetchone()
                if result and result[2] > 0:
                    articulos.append((result[0], result[1]))
                    total += result[1]
                else:
                    return HttpResponse(f"❌ Artículo con código {cod} no encontrado o sin stock.")

            if not articulos:
                return HttpResponse("❌ No se ingresaron artículos válidos.")

            if metodo_pago == "efectivo":
                if not monto_efectivo:
                    return HttpResponse("❌ Debe ingresar el monto entregado.")
                monto_efectivo = int(monto_efectivo)
                if monto_efectivo < total:
                    return HttpResponse("❌ Monto insuficiente.")
                vuelto = monto_efectivo - total
            elif metodo_pago in ["debito", "credito"] and not numero_operacion:
                return HttpResponse("❌ Debe ingresar el número de operación para pagos con tarjeta.")

            cursor.execute("INSERT INTO boleta (fecha, rut, id_vendedor) VALUES (%s, %s, %s)",
                           (date.today(), rut_cliente, id_vendedor))
            conexion.commit()
            id_boleta = cursor.lastrowid

            for id_articulo, precio in articulos:
                cursor.execute("INSERT INTO vendidos (id_boleta, id_articulo, cantidad, subtotal) VALUES (%s, %s, %s, %s)",
                               (id_boleta, id_articulo, 1, precio))
                cursor.execute("UPDATE articulo SET cantidad = cantidad - 1 WHERE id_articulo = %s", (id_articulo,))

            if metodo_pago in ["debito", "credito"]:
                cursor.execute("INSERT INTO ventas_tarjetas (id_boleta, numero_operacion, monto) VALUES (%s, %s, %s)",
                               (id_boleta, numero_operacion, total))

            conexion.commit()

            iva = round(total * 0.19)
            neto = total - iva

            mensaje = f"Pretty Fashion\nBOLETA N: {id_boleta}\nFecha: {date.today()}\nCliente: {rut_cliente}\n"
            for id_articulo, precio in articulos:
                mensaje += f"Artículo ID: {id_articulo} x1 = ${precio}\n"
            mensaje += f"Neto: ${neto}\nIVA (19%): ${iva}\nTotal: ${total}\n¡Gracias por su compra!\n\n\n\n\n\n\n"

            printer_name = "Boletera"
            hprinter = win32print.OpenPrinter(printer_name)
            job_info = ("Boleta", None, "RAW")
            win32print.StartDocPrinter(hprinter, 1, job_info)
            win32print.StartPagePrinter(hprinter)
            win32print.WritePrinter(hprinter, mensaje.encode("utf-8"))
            win32print.WritePrinter(hprinter, b'\x1D\x56\x00')
            win32print.EndPagePrinter(hprinter)
            win32print.EndDocPrinter(hprinter)
            win32print.ClosePrinter(hprinter)

            return HttpResponse("✅ Venta realizada e impresa correctamente.")

        except mysql.connector.Error as err:
            return HttpResponse(f"❌ Error de MySQL: {err}")
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conexion' in locals(): conexion.close()

    return render(request, "ventas/venta.html")

def calcular_total_ajax(request):
    if request.method == "POST":
        codigos = request.POST.get("codigos", "").strip().split("\n")
        total = 0
        try:
            conexion = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Sistemasinfo123",
                database="pretty_fashion"
            )
            cursor = conexion.cursor()
            for cod in codigos:
                cod = cod.strip()
                cursor.execute("SELECT precio FROM articulo WHERE codigo_barra = %s AND cantidad > 0", (cod,))
                result = cursor.fetchone()
                if result:
                    total += result[0]
        except:
            total = -1
        finally:
            if 'cursor' in locals(): cursor.close()
            if 'conexion' in locals(): conexion.close()
        return JsonResponse({"total": total})