# Generated by Django 5.0 on 2025-06-18 08:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('benefits', '0003_benefit_translations'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='benefit',
            name='benefit_for_entities_ca',
        ),
        migrations.RemoveField(
            model_name='benefit',
            name='benefit_for_entities_gl',
        ),
        migrations.RemoveField(
            model_name='benefit',
            name='benefit_for_members_ca',
        ),
        migrations.RemoveField(
            model_name='benefit',
            name='benefit_for_members_gl',
        ),
        migrations.RemoveField(
            model_name='benefit',
            name='discount_link_text_ca',
        ),
        migrations.RemoveField(
            model_name='benefit',
            name='discount_link_text_gl',
        ),
    ]
