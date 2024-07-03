# Generated by Django 5.0 on 2024-07-02 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_node_admin_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='multilang_enabled',
            field=models.BooleanField(default=False, verbose_name='Utiliza multi-idioma'),
        ),
        migrations.AddField(
            model_name='node',
            name='multilang_enabled_ca',
            field=models.BooleanField(default=False, verbose_name='Utiliza multi-idioma'),
        ),
        migrations.AddField(
            model_name='node',
            name='multilang_enabled_es',
            field=models.BooleanField(default=False, verbose_name='Utiliza multi-idioma'),
        ),
        migrations.AddField(
            model_name='node',
            name='multilang_enabled_eu',
            field=models.BooleanField(default=False, verbose_name='Utiliza multi-idioma'),
        ),
        migrations.AddField(
            model_name='node',
            name='multilang_enabled_gl',
            field=models.BooleanField(default=False, verbose_name='Utiliza multi-idioma'),
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
