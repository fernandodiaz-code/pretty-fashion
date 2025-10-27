# views.py (adaptado desde consola a vista Django)
from django.shortcuts import render, redirect
from django.http import HttpResponse
import mysql.connector

def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sistemasinfo123",
        database="pretty_fashion"
    )

def menu_inventario(request):
    return render(request, "inventario/menu.html")

def consultar_inventario(request):
    if request.method == "POST":
        conexion = conectar_bd()
        cursor = conexion.cursor()

        criterio = request.POST.get("criterio")
        resultados = []
        tipo_nombre = ""

        if criterio == 'codigo':
            codigo = request.POST.get("codigo")
            cursor.execute("""
                SELECT a.codigo, c.nombre_color,
                       COALESCE(ts.nombre_talla, tg.nombre_talla) AS talla,
                       t.tipo_de_prenda, a.cantidad
                FROM articulo a
                JOIN color c ON a.id_color = c.id_color
                JOIN tipo t ON a.id_tipo = t.id_tipo
                LEFT JOIN talla_sosten ts ON a.id_talla_sosten = ts.id_talla_sosten
                LEFT JOIN talla_general tg ON a.id_talla_general = tg.id_talla_general
                WHERE a.codigo = %s AND a.cantidad > 0
            """, (codigo,))
            resultados = cursor.fetchall()

        elif criterio == 'tipo_talla':
            tipo = request.POST.get("tipo")
            talla = request.POST.get("talla")
            cursor.execute("SELECT tipo_de_prenda FROM tipo WHERE id_tipo = %s", (tipo,))
            tipo_data = cursor.fetchone()
            tipo_nombre = tipo_data[0] if tipo_data else ""

            if tipo == '1':
                cursor.execute("""
                    SELECT a.codigo, c.nombre_color, ts.nombre_talla, t.tipo_de_prenda, a.cantidad
                    FROM articulo a
                    JOIN color c ON a.id_color = c.id_color
                    JOIN tipo t ON a.id_tipo = t.id_tipo
                    JOIN talla_sosten ts ON a.id_talla_sosten = ts.id_talla_sosten
                    WHERE a.id_tipo = %s AND ts.nombre_talla = %s AND a.cantidad > 0
                """, (tipo, talla))
            else:
                cursor.execute("""
                    SELECT a.codigo, c.nombre_color, tg.nombre_talla, t.tipo_de_prenda, a.cantidad
                    FROM articulo a
                    JOIN color c ON a.id_color = c.id_color
                    JOIN tipo t ON a.id_tipo = t.id_tipo
                    JOIN talla_general tg ON a.id_talla_general = tg.id_talla_general
                    WHERE a.id_tipo = %s AND tg.nombre_talla = %s AND a.cantidad > 0
                """, (tipo, talla))
            resultados = cursor.fetchall()

        cursor.close()
        conexion.close()

        return render(request, "inventario/consulta.html", {
            "resultados": resultados,
            "tipo_nombre": tipo_nombre
        })

    # GET: mostrar formulario de búsqueda
    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute("SELECT id_tipo, tipo_de_prenda FROM tipo")
    tipos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return render(request, "inventario/consulta.html", {"tipos": tipos})

def ingresar_stock(request):
    if request.method == "POST":
        codigos = request.POST.get("codigos", "").strip().split("\n")
        conexion = conectar_bd()
        cursor = conexion.cursor()
        mensajes = []

        for cod in codigos:
            cod = cod.strip()
            if cod == '':
                continue
            cursor.execute("SELECT id_articulo FROM articulo WHERE codigo_barra = %s", (cod,))
            articulo = cursor.fetchone()
            if articulo:
                cant = request.POST.get(f"cantidad_{cod}")
                try:
                    cantidad = int(cant)
                    cursor.execute("UPDATE articulo SET cantidad = cantidad + %s WHERE id_articulo = %s", (cantidad, articulo[0]))
                    mensajes.append(f"✅ {cod} actualizado con +{cantidad} unidades.")
                except ValueError:
                    mensajes.append(f"❌ Cantidad inválida para {cod}.")
            else:
                mensajes.append(f"❌ Código {cod} no encontrado.")

        conexion.commit()
        cursor.close()
        conexion.close()
        return render(request, "inventario/ingresar.html", {"mensajes": mensajes})

    return render(request, "inventario/ingresar.html")

def consultar_por_codigo(request):
    resultados = []
    if request.method == "POST":
        codigo = request.POST.get("codigo")
        conexion = conectar_bd()
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT a.codigo, c.nombre_color,
                   COALESCE(ts.nombre_talla, tg.nombre_talla) AS talla,
                   t.tipo_de_prenda, a.cantidad
            FROM articulo a
            JOIN color c ON a.id_color = c.id_color
            JOIN tipo t ON a.id_tipo = t.id_tipo
            LEFT JOIN talla_sosten ts ON a.id_talla_sosten = ts.id_talla_sosten
            LEFT JOIN talla_general tg ON a.id_talla_general = tg.id_talla_general
            WHERE a.codigo = %s AND a.cantidad > 0
        """, (codigo,))
        resultados = cursor.fetchall()

        cursor.close()
        conexion.close()

    return render(request, "inventario/consulta_codigo.html", {"resultados": resultados})

# ✅ NUEVA FUNCIÓN: consultar_por_tipo
def consultar_por_tipo(request):
    resultados = []
    tipo_nombre = ""
    tipos = []

    conexion = conectar_bd()
    cursor = conexion.cursor()
    cursor.execute("SELECT id_tipo, tipo_de_prenda FROM tipo")
    tipos = cursor.fetchall()

    if request.method == "POST":
        tipo = request.POST.get("tipo")
        talla = request.POST.get("talla")

        cursor.execute("SELECT tipo_de_prenda FROM tipo WHERE id_tipo = %s", (tipo,))
        tipo_data = cursor.fetchone()
        tipo_nombre = tipo_data[0] if tipo_data else ""

        if tipo == '1':
            cursor.execute("""
                SELECT a.codigo, c.nombre_color, ts.nombre_talla, t.tipo_de_prenda, a.cantidad
                FROM articulo a
                JOIN color c ON a.id_color = c.id_color
                JOIN tipo t ON a.id_tipo = t.id_tipo
                JOIN talla_sosten ts ON a.id_talla_sosten = ts.id_talla_sosten
                WHERE a.id_tipo = %s AND ts.nombre_talla = %s AND a.cantidad > 0
            """, (tipo, talla))
        else:
            cursor.execute("""
                SELECT a.codigo, c.nombre_color, tg.nombre_talla, t.tipo_de_prenda, a.cantidad
                FROM articulo a
                JOIN color c ON a.id_color = c.id_color
                JOIN tipo t ON a.id_tipo = t.id_tipo
                JOIN talla_general tg ON a.id_talla_general = tg.id_talla_general
                WHERE a.id_tipo = %s AND tg.nombre_talla = %s AND a.cantidad > 0
            """, (tipo, talla))

        resultados = cursor.fetchall()

    cursor.close()
    conexion.close()

    return render(request, "inventario/consulta_tipo.html", {
        "tipos": tipos,
        "resultados": resultados,
        "tipo_nombre": tipo_nombre
    })

def ingresar_stock(request):
    if request.method == "POST":
        codigos = request.POST.getlist("codigos[]")
        cantidades = request.POST.getlist("cantidades[]")
        conexion = conectar_bd()
        cursor = conexion.cursor()
        mensajes = []

        for codigo, cantidad_str in zip(codigos, cantidades):
            if not codigo.strip() or not cantidad_str.strip():
                continue
            try:
                cantidad = int(cantidad_str)
            except ValueError:
                mensajes.append(f"❌ Cantidad inválida para {codigo}")
                continue

            cursor.execute("SELECT id_articulo FROM articulo WHERE codigo_barra = %s", (codigo,))
            articulo = cursor.fetchone()
            if articulo:
                cursor.execute("UPDATE articulo SET cantidad = cantidad + %s WHERE id_articulo = %s", (cantidad, articulo[0]))
                mensajes.append(f"✅ Artículo con código {codigo} actualizado.")
            else:
                mensajes.append(f"❌ Código {codigo} no encontrado.")

        conexion.commit()
        cursor.close()
        conexion.close()
        return render(request, "inventario/ingresar.html", {"mensajes": mensajes})

    return render(request, "inventario/ingresar.html")