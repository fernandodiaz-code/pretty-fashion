import mysql.connector
from datetime import date
from pretty_fashion.printing import print_raw

def realizar_venta():
    try:
        # 1. Conexión a la base de datos
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Sistemasinfo123",
            database="pretty_fashion"
        )
        cursor = conexion.cursor()

        # 2. Ingreso de cliente
        rut_cliente = input("Ingrese RUT del cliente (o 777777777 si no desea registrarse): ")
        if rut_cliente != "777777777":
            cursor.execute("SELECT * FROM clientes WHERE rut_cliente = %s", (rut_cliente,))
            if not cursor.fetchone():
                nombre = input("Ingrese nombre del cliente: ")
                apellido = input("Ingrese apellido del cliente: ")
                cursor.execute("INSERT INTO clientes (rut_cliente, nombre, apellido) VALUES (%s, %s, %s)",
                               (rut_cliente, nombre, apellido))
                conexion.commit()

        # 3. Ingreso de artículos
        total_venta = 0
        articulos = []
        while True:
            cod_barra = input("Ingrese código de barra (o 'x' para terminar): ")
            if cod_barra.lower() == 'x':
                break

            cursor.execute("SELECT id_articulo, precio, cantidad FROM articulo WHERE codigo_barra = %s", (cod_barra,))
            result = cursor.fetchone()

            if not result:
                print("❌ Artículo no encontrado.")
            elif result[2] <= 0:
                print("❌ Artículo sin stock.")
            else:
                articulos.append((result[0], result[1]))
                total_venta += result[1]
                print("✅ Artículo agregado.")
            
        if not articulos:
            print("❌ No se ingresaron artículos.")
            return

        # 4. Confirmar método de pago
        print(f"\n💵 Total a pagar: ${total_venta}")
        print("\nMétodo de pago:")
        print("1. Débito")
        print("2. Crédito")
        print("3. Efectivo")
        metodo = input("Seleccione opción: ")

        # Calcular total
        total = sum(precio for _, precio in articulos)

        if metodo in ['1', '2']:
            num_operacion = input("Ingrese número de operación de la tarjeta: ")
        elif metodo == '3':
            pagado = int(input("Ingrese monto recibido: "))
            if pagado < total:
                print("❌ Monto insuficiente.")
                return
            vuelto = pagado - total
            print(f"💵 Vuelto a entregar: ${vuelto}")
        else:
            print("❌ Opción no válida.")
            return

        # 5. Insertar boleta
        id_vendedor = 1  # por ahora fijo
        cursor.execute("INSERT INTO boleta (fecha, rut, id_vendedor) VALUES (%s, %s, %s)",
                       (date.today(), rut_cliente, id_vendedor))
        conexion.commit()
        id_boleta = cursor.lastrowid

        # 6. Insertar ventas y actualizar stock
        for id_articulo, precio in articulos:
            cursor.execute("INSERT INTO vendidos (id_boleta, id_articulo, cantidad, subtotal) VALUES (%s, %s, %s, %s)",
                           (id_boleta, id_articulo, 1, precio))
            cursor.execute("UPDATE articulo SET cantidad = cantidad - 1 WHERE id_articulo = %s", (id_articulo,))
        conexion.commit()

        # 7. Insertar en ventas_tarjetas si corresponde
        if metodo in ['1', '2']:
            cursor.execute("INSERT INTO ventas_tarjetas (id_boleta, numero_operacion, monto) VALUES (%s, %s, %s)",
                           (id_boleta, num_operacion, total))
            conexion.commit()

        # 8. Imprimir boleta
        mensaje = f"Pretty Fashion\nBOLETA N: {id_boleta}\nFecha: {date.today()}\nCliente: {rut_cliente}\n"
        for id_articulo, precio in articulos:
            mensaje += f"Artículo ID: {id_articulo} x1 = ${precio}\n"
        mensaje += f"Total: ${total}\n¡Gracias por su compra!\n\n\n\n\nn\n\n\n"

        print_raw(mensaje)

        print("✅ Venta realizada e impresa correctamente.")

    except mysql.connector.Error as err:
        print(f"❌ Error de MySQL: {err}")
    finally:
        if cursor: cursor.close()
        if conexion: conexion.close()

# Ejecutar
realizar_venta()



  
