from django.shortcuts import render
from django.db import connection
from datetime import datetime

# Menú principal
def menu_vendedores(request):
    return render(request, 'vendedores/menu.html')

# Lista de vendedores
def lista_vendedores(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_vendedor, nombre, apellido FROM vendedor")
        vendedores = cursor.fetchall()
    return render(request, 'vendedores/lista.html', {'vendedores': vendedores})

# Boletas emitidas por un vendedor seleccionado desde formulario
def boletas_por_vendedor(request):
    vendedores = []
    boletas = []
    id_vendedor = None
    nombre_vendedor = ""

    # Obtener todos los vendedores
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_vendedor, nombre, apellido FROM vendedor")
        vendedores = cursor.fetchall()

    if request.method == 'POST':
        id_vendedor = request.POST.get('id_vendedor')

        if id_vendedor:
            with connection.cursor() as cursor:
                # Boletas emitidas por el vendedor
                cursor.execute("""
                    SELECT b.id_boleta, b.fecha, SUM(v.subtotal) AS total
                    FROM boleta b
                    JOIN vendidos v ON b.id_boleta = v.id_boleta
                    WHERE b.id_vendedor = %s
                    GROUP BY b.id_boleta, b.fecha
                    ORDER BY b.fecha DESC
                """, [id_vendedor])
                boletas = cursor.fetchall()

                # Obtener nombre del vendedor
                cursor.execute("SELECT nombre, apellido FROM vendedor WHERE id_vendedor = %s", [id_vendedor])
                result = cursor.fetchone()
                if result:
                    nombre_vendedor = f"{result[0]} {result[1]}"

    return render(request, 'vendedores/boletas.html', {
        'boletas': boletas,
        'vendedores': vendedores,
        'id_vendedor': id_vendedor,
        'nombre_vendedor': nombre_vendedor
    })

# Ventas por rango de fechas: muestra el total vendido
def ventas_por_vendedor(request):
    total_ventas = None
    vendedores = []
    fecha_inicio = fecha_fin = id_vendedor = None
    nombre_vendedor = ""

    # Cargar lista de vendedores
    with connection.cursor() as cursor:
        cursor.execute("SELECT id_vendedor, nombre, apellido FROM vendedor")
        vendedores = cursor.fetchall()

    if request.method == 'POST':
        id_vendedor = request.POST.get('id_vendedor')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        if id_vendedor and fecha_inicio and fecha_fin:
            try:
                datetime.strptime(fecha_inicio, '%Y-%m-%d')
                datetime.strptime(fecha_fin, '%Y-%m-%d')

                with connection.cursor() as cursor:
                    # Calcular total de ventas
                    cursor.execute("""
                        SELECT SUM(v.subtotal)
                        FROM boleta b
                        JOIN vendidos v ON b.id_boleta = v.id_boleta
                        WHERE b.id_vendedor = %s AND b.fecha BETWEEN %s AND %s
                    """, [id_vendedor, fecha_inicio, fecha_fin])
                    total_ventas = cursor.fetchone()[0] or 0

                    # Nombre del vendedor
                    cursor.execute("SELECT nombre, apellido FROM vendedor WHERE id_vendedor = %s", [id_vendedor])
                    result = cursor.fetchone()
                    if result:
                        nombre_vendedor = f"{result[0]} {result[1]}"

            except ValueError:
                return render(request, 'vendedores/ventas.html', {
                    'mensaje': "Fechas inválidas",
                    'vendedores': vendedores
                })

    return render(request, 'vendedores/ventas.html', {
        'total_ventas': total_ventas,
        'vendedores': vendedores,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'id_vendedor': id_vendedor,
        'nombre_vendedor': nombre_vendedor
    })
