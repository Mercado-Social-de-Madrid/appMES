# Generated by Django 5.0 on 2024-02-22 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_node_add_webpage_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='info_page_url',
            field=models.TextField(blank=True, null=True, verbose_name='Enlace a página con información básica del mercado'),
        ),
        migrations.AddField(
            model_name='node',
            name='member_card_enabled',
            field=models.BooleanField(default=True, verbose_name='Carnet de socia activa'),
        ),
    ]
