from django.shortcuts import render, redirect
import win32print
import win32ui
from django.db import connection

# Menú principal de Jefatura
def menu_jefatura(request):
    return render(request, 'jefatura/menu.html')

# Vista para emitir nota de crédito
def nota_credito(request):
    mensaje = ""
    if request.method == 'POST':
        numero_boleta = request.POST.get('numero_boleta')
        motivo = request.POST.get('motivo')

        if numero_boleta and motivo:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id_boleta FROM boleta WHERE id_boleta = %s", [numero_boleta])
                boleta = cursor.fetchone()

            if boleta:
                id_boleta = boleta[0]

                # Calcular el total sumando subtotales de la tabla vendidos
                with connection.cursor() as cursor:
                    cursor.execute("""
                        SELECT SUM(subtotal) FROM vendidos WHERE id_boleta = %s
                    """, [id_boleta])
                    total = cursor.fetchone()[0] or 0

                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO nota_credito (id_boleta, motivo, monto_devuelto)
                        VALUES (%s, %s, %s)
                    """, [id_boleta, motivo, total])

                try:
                    printer_name = "Boletera"
                    pdc = win32ui.CreateDC()
                    pdc.CreatePrinterDC(printer_name)
                    pdc.StartDoc("Nota de Crédito")
                    pdc.StartPage()
                    pdc.TextOut(100, 100, "***** NOTA DE CREDITO *****")
                    pdc.TextOut(100, 200, f"Boleta anulada: {id_boleta}")
                    pdc.TextOut(100, 300, f"Motivo: {motivo}")
                    pdc.TextOut(100, 400, f"Total devuelto: ${total}")
                    pdc.TextOut(100, 500, "Gracias por su preferencia")
                    pdc.EndPage()
                    pdc.EndDoc()
                    pdc.DeleteDC()
                except Exception as e:
                    mensaje = f"Nota registrada pero falló la impresión: {str(e)}"
                else:
                    mensaje = "Nota de crédito emitida con éxito"
            else:
                mensaje = "Boleta no encontrada"
        else:
            mensaje = "Debe ingresar número de boleta y motivo"

    return render(request, 'jefatura/nota_credito.html', {'mensaje': mensaje})

# Vista para listar y eliminar vendedores
def gestion_vendedores_admin(request):
    mensaje = ""
    if request.method == 'POST' and 'eliminar' in request.POST:
        id_vendedor = request.POST.get('eliminar')
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM vendedor WHERE id_vendedor = %s", [id_vendedor])
        mensaje = "Vendedor eliminado correctamente."

    with connection.cursor() as cursor:
        cursor.execute("SELECT id_vendedor, nombre, apellido FROM vendedor")
        vendedores = cursor.fetchall()

    return render(request, 'jefatura/gestion_vendedores.html', {
        'vendedores': vendedores,
        'mensaje': mensaje
    })

# Vista para agregar un nuevo vendedor
def agregar_vendedor(request):
    mensaje = ""
    if request.method == 'POST':
        id_vendedor = request.POST.get('id_vendedor')
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')

        if id_vendedor and nombre and apellido:
            try:
                with connection.cursor() as cursor:
                    cursor.execute("""
                        INSERT INTO vendedor (id_vendedor, nombre, apellido)
                        VALUES (%s, %s, %s)
                    """, [id_vendedor, nombre, apellido])
                return redirect('gestion_vendedores_admin')
            except Exception as e:
                mensaje = f"Error al agregar vendedor: {str(e)}"
        else:
            mensaje = "Debe completar todos los campos."

    return render(request, 'jefatura/agregar_vendedor.html', {
        'mensaje': mensaje
    })

# Vista para modificar inventario por robo
def modificar_inventario_robo(request):
    mensaje = ""
    if request.method == 'POST':
        codigo_barra = request.POST.get('codigo_barra')
        cantidad = int(request.POST.get('cantidad'))

        with connection.cursor() as cursor:
            # Verificar existencia del artículo
            cursor.execute("""
                SELECT cantidad FROM articulo WHERE codigo_barra = %s
            """, [codigo_barra])
            articulo = cursor.fetchone()

            if articulo:
                stock_actual = articulo[0]
                if cantidad > stock_actual:
                    mensaje = f"No se puede descontar {cantidad}. Solo hay {stock_actual} en stock."
                else:
                    # Descontar del stock
                    cursor.execute("""
                        UPDATE articulo
                        SET cantidad = cantidad - %s
                        WHERE codigo_barra = %s
                    """, [cantidad, codigo_barra])
                    mensaje = "Inventario actualizado correctamente."
            else:
                mensaje = "El artículo con ese código de barra no existe."

    return render(request, 'jefatura/modificar_inventario_robo.html', {'mensaje': mensaje})

# Vista para otras funciones administrativas
def gestion_general_sistema(request):
    return render(request, 'jefatura/gestion_general_sistema.html')
