# Conexion Django con Supabase

## Requisitos

- URL del proyecto Supabase
- host, puerto, base, usuario y password de PostgreSQL
- paquete Python psycopg

## Configuracion objetivo

DATABASES debera usar:

- ENGINE = django.db.backends.postgresql
- NAME
- USER
- PASSWORD
- HOST
- PORT = 5432

## Orden recomendado

1. Crear el proyecto Supabase.
2. Ejecutar supabase/schema.sql en el SQL editor.
3. Instalar psycopg.
4. Configurar variables de entorno para credenciales.
5. Ejecutar chequeos de Django.
6. Migrar vistas desde SQL manual hacia ORM por modulos.

## Datos que faltan para conectar de verdad

- proyecto Supabase creado
- credenciales de conexion PostgreSQL
- decision sobre si usaremos public o un schema propio
