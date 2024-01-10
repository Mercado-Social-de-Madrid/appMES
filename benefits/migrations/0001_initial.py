# Generated by Django 5.0 on 2024-01-10 12:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('market', '0002_consumer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Benefit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('published_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('benefit_for_entities', models.TextField(blank=True, null=True, verbose_name='Ventajas para entidades')),
                ('benefit_for_members', models.TextField(blank=True, null=True, verbose_name='Ventajas para socias')),
                ('includes_intercoop_members', models.BooleanField(default=False, verbose_name='Incluye socias Intercoop')),
                ('in_person', models.BooleanField(default=True, verbose_name='Solicitud física')),
                ('online', models.BooleanField(default=True, verbose_name='Solicitud online')),
                ('discount_code', models.CharField(blank=True, max_length=500, null=True, verbose_name='Código de descuento')),
                ('discount_link_entities', models.CharField(blank=True, max_length=200, null=True, verbose_name='Link de descuento para entidades')),
                ('discount_link_members', models.CharField(blank=True, max_length=200, null=True, verbose_name='Link de descuento para socias')),
                ('discount_link_text', models.CharField(blank=True, default='Solicitar descuento', max_length=100, null=True, verbose_name='Texto del botón del link de descuento')),
                ('active', models.BooleanField(default=True, verbose_name='Activa')),
                ('entity', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='benefit', to='market.provider')),
            ],
            options={
                'verbose_name': 'Ventaja',
                'verbose_name_plural': 'Ventajas',
                'ordering': ['-published_date'],
            },
        ),
    ]
