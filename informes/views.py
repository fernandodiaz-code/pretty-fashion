from django.shortcuts import render
from django.db import connection

def menu_informes(request):
    return render(request, 'informes/menu_informes.html')

def informe_ventas(request):
    total = None  # Inicializar total

    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        print(f"Fechas recibidas: {fecha_inicio} {fecha_fin}")

        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT SUM(ven.subtotal)
                FROM boleta b
                JOIN vendidos ven ON b.id_boleta = ven.id_boleta
                WHERE b.fecha BETWEEN %s AND %s
            """, [fecha_inicio, fecha_fin])
            
            resultado = cursor.fetchone()
            total = resultado[0] if resultado[0] is not None else 0

        print(f"Total calculado: {total}")

    return render(request, 'informes/informe_ventas.html', {
        'total': total
    })




def informe_notas_credito(request):
    datos = []
    total_notas = 0
    monto_total_devuelto = 0

    if request.method == 'POST':
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        with connection.cursor() as cursor:
            # Obtener detalles de cada nota
            cursor.execute("""
                SELECT nc.id_nota_credito, nc.fecha, nc.motivo, nc.monto_devuelto, b.rut
                FROM nota_credito nc
                JOIN boleta b ON nc.id_boleta = b.id_boleta
                WHERE nc.fecha BETWEEN %s AND %s
                ORDER BY nc.fecha DESC
            """, [fecha_inicio, fecha_fin])
            datos = cursor.fetchall()

            # Obtener totales
            cursor.execute("""
                SELECT COUNT(*), SUM(nc.monto_devuelto)
                FROM nota_credito nc
                WHERE nc.fecha BETWEEN %s AND %s
            """, [fecha_inicio, fecha_fin])
            resultado = cursor.fetchone()
            total_notas = resultado[0]
            monto_total_devuelto = resultado[1] if resultado[1] else 0

    return render(request, 'informes/informe_notas.html', {
        'datos': datos,
        'total_notas': total_notas,
        'monto_total_devuelto': monto_total_devuelto
    })
