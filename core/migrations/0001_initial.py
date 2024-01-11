from django.db import migrations


def load_admin_theme(apps, schema_editor):
    # Load the fixture using the `loaddata` management command
    from django.core.management import call_command
    call_command('loaddata', 'admin_interface_theme_mes.json', app='core')


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.RunPython(load_admin_theme),
    ]

