# Generated by Django 5.0 on 2024-01-25 12:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('benefits', '0001_initial'),
        ('market', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='benefit',
            name='entity',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='benefit', to='market.provider'),
        ),
    ]