# Generated by Django 5.1.11 on 2025-06-18 11:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_intercoop'),
        ('market', '0012_remove_unused_langs'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='consumer',
            options={'ordering': ['-registration_date'], 'verbose_name': 'Consumidora', 'verbose_name_plural': 'Consumidoras'},
        ),
        migrations.CreateModel(
            name='Intercoop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField(auto_now_add=True, null=True, verbose_name='Fecha de creación')),
                ('name', models.CharField(blank=True, max_length=250, null=True, verbose_name='Nombre')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Condiciones de intercooperación')),
                ('external_id_needed', models.BooleanField(default=True, verbose_name='Incluir identificador de socia externa para validación')),
                ('external_id_label', models.CharField(blank=True, max_length=200, null=True, verbose_name='Etiqueta del identificador en el formulario')),
                ('external_id_label_es', models.CharField(blank=True, max_length=200, null=True, verbose_name='Etiqueta del identificador en el formulario')),
                ('external_id_label_eu', models.CharField(blank=True, max_length=200, null=True, verbose_name='Etiqueta del identificador en el formulario')),
                ('node', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.node')),
                ('provider', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='market.provider', verbose_name='Entidad proveedora de intercooperación')),
            ],
            options={
                'verbose_name': 'Proveedora de intercooperación',
                'verbose_name_plural': 'Proveedoras de intercooperación',
                'ordering': ['name'],
            },
        ),
    ]
