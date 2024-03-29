# Generated by Django 5.0 on 2024-01-31 12:08

import helpers.filesystem
import imagekit.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_add_admin_themes'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='banner_image',
            field=imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=helpers.filesystem.RandomFileName('node/'), verbose_name='Imagen principal'),
        ),
        migrations.AddField(
            model_name='node',
            name='contact_email',
            field=models.EmailField(blank=True, max_length=200, null=True, verbose_name='Email de contacto'),
        ),
        migrations.AddField(
            model_name='node',
            name='preferred_locale',
            field=models.CharField(default='es-ES', max_length=10, verbose_name='Idioma preferido de la interfaz'),
        ),
        migrations.AddField(
            model_name='node',
            name='register_consumer_url',
            field=models.TextField(blank=True, null=True, verbose_name='Enlace al formulario de registro de consumidoras'),
        ),
        migrations.AddField(
            model_name='node',
            name='register_provider_url',
            field=models.TextField(blank=True, null=True, verbose_name='Enlace al formulario de registro de proveedoras'),
        ),
        migrations.AddField(
            model_name='node',
            name='self_register_allowed',
            field=models.BooleanField(default=False, verbose_name='Permitir el registro abierto'),
        ),
    ]
