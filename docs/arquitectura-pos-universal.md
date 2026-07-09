# Pretty Fashion como POS universal

## Idea central

Pretty Fashion sera la primera implementacion de un punto de venta adaptable. El sistema base debe servir para rubros distintos sin cambiar el nucleo de datos cada vez.

## Nucleo del sistema

- sucursales
- usuarios
- clientes
- categorias
- productos
- atributos
- valores de atributo
- variantes de producto
- stock por variante y sucursal
- ventas
- detalle de venta
- pagos
- devoluciones

## Como representa Pretty Fashion sus casos especiales

Pretty Fashion puede definir atributos como talla, copa, color y tipo de prenda.

Una variante concreta podria ser: producto = sosten basico, talla = 36, copa = C, color = negro.

Otro cliente podria usar el mismo sistema con: producto = bebida cola, sabor = cola, formato = 1.5L.

La base no necesita cambiar entre ambos negocios.

## Decisiones de diseno

- PostgreSQL en Supabase sera la base de datos objetivo.
- Las variantes son las unidades vendibles y stockeables.
- Los atributos son configurables por producto.
- El stock vive por variante y sucursal.
- Las ventas guardan una copia de nombre, SKU y precio para conservar historia aunque el catalogo cambie despues.
- Las devoluciones se modelan separadas de las ventas.

## Proximo paso tecnico

1. Crear el proyecto Supabase.
2. Ejecutar supabase/schema.sql.
3. Configurar Django con PostgreSQL.
4. Migrar las vistas actuales desde SQL manual al ORM nuevo por modulos.
