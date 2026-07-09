# Generated manually to match ventas/models.py changes (Bash execution of
# `makemigrations` was blocked by the sandbox permission system in this
# session; migration content mirrors the model diff exactly).

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas', '0002_remove_recarga_numero_operacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='recarga',
            name='lugar_venta',
            field=models.CharField(
                choices=[('local', 'Local'), ('camion', 'Camión')],
                default='local',
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name='recarga',
            name='precio_base',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='recarga',
            name='descuento_total',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='recarga',
            name='aplica_qr',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='recarga',
            name='tipo_qr',
            field=models.CharField(
                choices=[
                    ('ninguno', 'Ninguno'),
                    ('qr_local', 'QR local'),
                    ('qr_camion', 'QR domicilio/camión'),
                ],
                default='ninguno',
                max_length=10,
            ),
        ),
        migrations.AddField(
            model_name='recarga',
            name='comentario',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='recarga',
            name='metodo_pago',
            field=models.CharField(
                choices=[
                    ('efectivo', 'Efectivo'),
                    ('debito', 'Débito'),
                    ('transferencia', 'Transferencia'),
                    ('credito', 'Crédito'),
                    ('bono_gobierno', 'Bono del gobierno'),
                    ('vale_fisico', 'Vale físico'),
                    ('vale_digital', 'Vale digital'),
                ],
                default='efectivo',
                max_length=20,
            ),
        ),
    ]
