# Generated by Django 5.0 on 2024-01-24 11:08

import django.db.models.deletion
import helpers.filesystem
import imagekit.models.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=250, null=True, verbose_name='Título (máx 200 caracteres)')),
                ('short_description', models.TextField(blank=True, null=True, verbose_name='Descripción corta')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Descripción')),
                ('banner_image', imagekit.models.fields.ProcessedImageField(blank=True, null=True, upload_to=helpers.filesystem.RandomFileName('news/'), verbose_name='Imagen principal')),
                ('published_date', models.DateTimeField(auto_now_add=True)),
                ('more_info_text', models.CharField(blank=True, max_length=250, null=True, verbose_name='Texto del botón de info')),
                ('more_info_url', models.TextField(blank=True, null=True, verbose_name='URL con más información')),
                ('node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.node', verbose_name='Mercado en el que se publica')),
                ('published_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Noticia',
                'verbose_name_plural': 'Noticias',
                'ordering': ['-published_date'],
            },
        ),
    ]
