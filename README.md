# Gas Orteguita

Sistema Django para gestion de ventas, inventario, vendedores, jefatura e informes de Gas Orteguita.

## Instalacion local

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Abrir:

```text
http://127.0.0.1:8000/login/
```

## Configuracion

Variables de entorno opcionales:

```bash
export DJANGO_SECRET_KEY="change-me"
```

La base de datos local `db.sqlite3`, el entorno virtual `.venv/` y archivos `.env` no se versionan.

## API movil

La API usa sesion autenticada de Django:

- `GET /api/ventas/config/`
- `POST /api/ventas/`

Tambien queda montada bajo `/apiventas/` por compatibilidad.
