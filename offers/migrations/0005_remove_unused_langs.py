# Generated by Django 5.0 on 2025-06-18 08:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('offers', '0004_offer_translations'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='offer',
            name='description_ca',
        ),
        migrations.RemoveField(
            model_name='offer',
            name='description_gl',
        ),
        migrations.RemoveField(
            model_name='offer',
            name='title_ca',
        ),
        migrations.RemoveField(
            model_name='offer',
            name='title_gl',
        ),
    ]
