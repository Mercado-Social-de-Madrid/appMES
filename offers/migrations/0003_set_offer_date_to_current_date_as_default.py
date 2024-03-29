# Generated by Django 5.0 on 2024-03-19 12:59

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0002_alter_offer_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='begin_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Fecha de inicio'),
        ),
        migrations.AlterField(
            model_name='offer',
            name='end_date',
            field=models.DateField(blank=True, default=django.utils.timezone.now, null=True, verbose_name='Fecha de fin'),
        ),
    ]
