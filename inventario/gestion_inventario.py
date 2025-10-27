import mysql.connector

def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sistemasinfo123",
        database="pretty_fashion"
    )

def consultar_inventario():
    conexion = conectar_bd()
    cursor = conexion.cursor()

    print("\n🔍 CONSULTA DE INVENTARIO")
    print("1. Buscar por código de artículo")
    print("2. Buscar por tipo y talla")
    opcion = input("Seleccione una opción: ")

    if opcion == '1':
        codigo = input("Ingrese código del producto: ")
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
    elif opcion == '2':
        print("\n📋 Tipos disponibles:")
        cursor.execute("SELECT id_tipo, tipo_de_prenda FROM tipo")
        tipos = cursor.fetchall()
        for t in tipos:
            print(f"{t[0]} - {t[1]}")

        tipo = input("Ingrese ID del tipo: ")
        cursor.execute("SELECT tipo_de_prenda FROM tipo WHERE id_tipo = %s", (tipo,))
        tipo_nombre = cursor.fetchone()
        if not tipo_nombre:
            print("❌ Tipo no encontrado.")
            return

        talla_valida = False
        while not talla_valida:
            talla = input("Ingrese nombre exacto de la talla: ")
            if tipo == '1':
                cursor.execute("SELECT id_talla_sosten FROM talla_sosten WHERE nombre_talla = %s", (talla,))
                talla_valida = cursor.fetchone()
            else:
                cursor.execute("SELECT id_talla_general FROM talla_general WHERE nombre_talla = %s", (talla,))
                talla_valida = cursor.fetchone()

            if not talla_valida:
                print("❌ Talla no válida para el tipo seleccionado. Intente nuevamente.")

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
    else:
        print("❌ Opción inválida.")
        return

    resultados = cursor.fetchall()
    if resultados:
        print("\n📦 Artículos disponibles:")
        for r in resultados:
            print(f"📌 Código: {r[0]}, Color: {r[1]}, Talla: {r[2]}, Tipo: {r[3]}, Cantidad: {r[4]}")
    else:
        print("❌ No hay artículos disponibles con esos criterios.")

    cursor.close()
    conexion.close()

def ingresar_stock():
    conexion = conectar_bd()
    cursor = conexion.cursor()

    print("\n📥 INGRESO DE ARTÍCULOS AL INVENTARIO")
    codigos = []

    while True:
        cod_barra = input("Ingrese código de barra (o 'x' para finalizar): ")
        if cod_barra.lower() == 'x':
            break
        codigos.append(cod_barra)

    for cod in codigos:
        cursor.execute("SELECT id_articulo FROM articulo WHERE codigo_barra = %s", (cod,))
        articulo = cursor.fetchone()
        if articulo:
            try:
                cant = int(input(f"Ingrese cantidad a agregar para código {cod}: "))
                cursor.execute("UPDATE articulo SET cantidad = cantidad + %s WHERE id_articulo = %s", (cant, articulo[0]))
                print(f"✅ Artículo con código {cod} actualizado.")
            except ValueError:
                print("❌ Cantidad inválida.")
        else:
            print(f"❌ Código {cod} no encontrado.")

    conexion.commit()
    cursor.close()
    conexion.close()
    print("📌 Actualización completada.")

def menu_inventario():
    while True:
        print("\n==== MENÚ INVENTARIO ====")
        print("1. Consultar inventario")
        print("2. Ingresar artículos al inventario")
        print("3. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            consultar_inventario()
        elif opcion == '2':
            ingresar_stock()
        elif opcion == '3':
            print("👋 Saliendo del menú.")
            break
        else:
            print("❌ Opción inválida.")

# Ejecutar si se llama directamente
if __name__ == "__main__":
    menu_inventario()

