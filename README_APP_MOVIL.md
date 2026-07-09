# App movil Gasort

## Objetivo

La app movil sera una extension de Gasort para trabajadores, repartidores o vendedores. Su alcance es registrar ventas desde Android/iOS sin incluir funciones administrativas.

El administrador seguira usando Gasort web para inventario, precios, vendedores, informes y gestion general.

## Arquitectura

\`\`\`text
Flutter App
  -> API REST Django
  -> SQLite actual
  -> futura migracion a Supabase/PostgreSQL
\`\`\`

La API usa la misma logica de negocio que el formulario web de ventas. Para evitar duplicacion, la regla de registro vive en \`ventas/services.py\` y es reutilizada por:

- \`ventas/views.py\`: formulario web actual.
- \`ventas/api_views.py\`: endpoints JSON para la app movil.

## Estado actual

- Backend: Django 5.2.1.
- Base de datos: SQLite \`db.sqlite3\`.
- App movil propuesta: Flutter.
- API implementada sin Django REST Framework para evitar dependencias nuevas en esta etapa.

## Endpoints creados

Todos los endpoints requieren sesion Django autenticada.

### \`GET /api/ventas/config/\`

Entrega datos necesarios para renderizar el formulario movil:

- galones disponibles;
- stock;
- precios actuales;
- estados recibidos;
- lugares de venta;
- metodos de pago;
- descuentos QR fijos.

### \`POST /api/ventas/\`

Registra una venta.

Body JSON esperado:

\`\`\`json
{
  "peso": 11,
  "estado_recibido": "vacio",
  "lugar_venta": "local",
  "metodo_pago": "efectivo",
  "pago_mixto": false,
  "metodo_pago_2": "",
  "monto_pago_1": 0,
  "monto_pago_2": 0,
  "aplica_qr": false,
  "descuento_manual": 0,
  "comentario": ""
}
\`\`\`

## Flujo de venta

1. La app carga configuracion desde \`/api/ventas/config/\`.
2. El trabajador selecciona peso, estado recibido, lugar de venta y metodo de pago.
3. La app calcula una vista previa del total, pero Django recalcula todo al registrar.
4. La app envia la venta a \`/api/ventas/\`.
5. Django valida datos, precio, descuento, stock y pago mixto.
6. Django actualiza inventario: \`llenos -1\`, \`vacios +1\` o \`conchos +1\`.
7. Django crea el registro \`Recarga\`.
8. La venta queda visible en Gasort web para administrador e informes.

## Como ejecutar Django

\`\`\`bash
cd /home/agente-de-fer/Escritorio/proyectos/gasort
.venv/bin/python manage.py runserver 0.0.0.0:8000
\`\`\`

## Como ejecutar Flutter

Pendiente para la etapa de creacion de app.

Cuando exista el proyecto Flutter:

\`\`\`bash
flutter pub get
flutter run
\`\`\`

## Seguridad

Estado actual:

- La API requiere sesion Django autenticada.
- No se agrego token movil todavia.
- No se modifico \`settings.py\`.
- No se instalaron dependencias nuevas.

Pendiente recomendado:

- crear login API para trabajadores;
- definir si se usara sesion Django, token simple o JWT;
- separar usuarios reales de Django y \`StaffUser\`, o vincularlos formalmente;
- agregar CORS solo si la app lo necesita en entorno web/debug.

## Consideraciones para Supabase

La app Flutter no debe conectarse directo a Supabase en esta fase. Debe hablar con Django para conservar reglas de negocio centralizadas.

Cuando se migre a Supabase/PostgreSQL:

1. Cambiar \`DATABASES\` en Django.
2. Migrar datos desde SQLite.
3. Mantener endpoints Flutter iguales.
4. Verificar transacciones de stock con PostgreSQL.
5. Ajustar autenticacion si se decide usar Supabase Auth.

## Riesgos y pendientes

- SQLite sirve para desarrollo y uso local, pero no es ideal para muchos moviles escribiendo al mismo tiempo.
- Falta implementar app Flutter.
- Falta login movil.
- Falta definir asociacion de venta con vendedor autenticado.
- Falta probar desde un dispositivo fisico en la misma red.
