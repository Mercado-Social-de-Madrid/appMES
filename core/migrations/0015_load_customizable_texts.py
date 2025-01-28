from django.core.management import call_command
from django.db import migrations


def load_custom_texts(apps, schema_editor):
    call_command('loaddata', 'custom_texts.json', app='core')

def unload_custom_texts(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_customizable_text'),
    ]

    operations = [
        migrations.RunPython(load_custom_texts, unload_custom_texts),
    ]
