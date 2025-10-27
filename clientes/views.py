from django.shortcuts import render
from django.db import connection

def consultar_boletas_por_rut_web(request):
    datos_cliente = None
    boletas = []
    rut = ''
    mensaje = ''

    if request.method == 'POST':
        rut = request.POST.get('rut')

        with connection.cursor() as cursor:
            cursor.execute("SELECT nombre, apellido FROM clientes WHERE rut_cliente = %s", [rut])
            cliente = cursor.fetchone()

            if not cliente:
                mensaje = "Cliente no encontrado."
            else:
                datos_cliente = {
                    'nombre': cliente[0],
                    'apellido': cliente[1],
                    'rut': rut
                }

                cursor.execute("""
                    SELECT id_boleta FROM boleta WHERE rut = %s ORDER BY id_boleta
                """, [rut])
                boletas_raw = cursor.fetchall()

                for (id_boleta,) in boletas_raw:
                    cursor.execute("""
                        SELECT a.codigo, v.cantidad, v.subtotal
                        FROM vendidos v
                        JOIN articulo a ON v.id_articulo = a.id_articulo
                        WHERE v.id_boleta = %s
                    """, [id_boleta])
                    articulos = cursor.fetchall()
                    total = sum(subtotal for _, _, subtotal in articulos)

                    boletas.append({
                        'id': id_boleta,
                        'articulos': [{'codigo': cod, 'cantidad': cant, 'subtotal': subtotal} for cod, cant, subtotal in articulos],
                        'total': total
                    })

    return render(request, 'clientes/consultar_boletas.html', {
        'datos_cliente': datos_cliente,
        'boletas': boletas,
        'mensaje': mensaje,
        'rut': rut
    })
