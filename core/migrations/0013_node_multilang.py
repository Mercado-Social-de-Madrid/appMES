# Generated by Django 5.0 on 2024-07-12 07:39

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_node_admin_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='enabled_langs',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('es', 'Castellano'), ('ca', 'Catalá'), ('eu', 'Euskara'), ('gl', 'Galego')], max_length=3), blank=True, default=[], size=None, verbose_name='Idiomas habilitados'),
        ),
        migrations.AddField(
            model_name='node',
            name='name_ca',
            field=models.CharField(max_length=150, null=True, verbose_name='Nombre'),
        ),
        migrations.AddField(
            model_name='node',
            name='name_es',
            field=models.CharField(max_length=150, null=True, verbose_name='Nombre'),
        ),
        migrations.AddField(
            model_name='node',
            name='name_eu',
            field=models.CharField(max_length=150, null=True, verbose_name='Nombre'),
        ),
        migrations.AddField(
            model_name='node',
            name='name_gl',
            field=models.CharField(max_length=150, null=True, verbose_name='Nombre'),
        ),
    ]
