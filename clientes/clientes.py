 
# clientes/clientes.py

import mysql.connector

def conectar_bd():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Sistemasinfo123",
        database="pretty_fashion"
    )

def consultar_boletas_por_rut():
    conexion = conectar_bd()
    cursor = conexion.cursor()

    while True:
        rut = input("Ingrese el RUT del cliente: ")

        cursor.execute("SELECT nombre, apellido FROM clientes WHERE rut_cliente = %s", (rut,))
        cliente = cursor.fetchone()
        if not cliente:
            print("❌ Cliente no encontrado.")
        else:
            print(f"\n👤 Cliente: {cliente[0]} {cliente[1]}\n")

            cursor.execute("""
                SELECT b.id_boleta
                FROM boleta b
                WHERE b.rut = %s
                ORDER BY b.id_boleta
            """, (rut,))
            boletas = cursor.fetchall()

            if not boletas:
                print("❌ No hay boletas asociadas a este cliente.")
            else:
                for (id_boleta,) in boletas:
                    print(f"🧾 Boleta N°: {id_boleta}")

                    cursor.execute("""
                        SELECT a.codigo, v.cantidad, v.subtotal
                        FROM vendidos v
                        JOIN articulo a ON v.id_articulo = a.id_articulo
                        WHERE v.id_boleta = %s
                    """, (id_boleta,))
                    articulos = cursor.fetchall()

                    total = 0
                    for cod, cant, subtotal in articulos:
                        print(f"🛍 Código: {cod} | Cantidad: {cant} | Subtotal: ${subtotal}")
                        total += subtotal

                    print(f"💵 Total boleta: ${total}")
                    print("-" * 30)

        # Preguntar si quiere buscar otro cliente
        continuar = input("\n¿Desea buscar otro cliente? (s/n): ").lower()
        if continuar != 's':
            print("👋 Fin de la consulta de clientes.")
            break

    cursor.close()
    conexion.close()

# Ejecutar si se llama directamente
if __name__ == "__main__":
    consultar_boletas_por_rut()
