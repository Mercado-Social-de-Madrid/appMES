import bz2
import json
import os

from django.db import migrations

FIXTURES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'fixtures', 'cities_light')

# Loaded in dependency order. Fixtures generated with `cities_light` (CITIES_LIGHT_CITY_SOURCES=cities500, ES only)
# followed by `cities_light_fixtures dump`
MODELS = [
    ('Country', 'cities_light_country.json.bz2'),
    ('Region', 'cities_light_region.json.bz2'),
    ('SubRegion', 'cities_light_subregion.json.bz2'),
    ('City', 'cities_light_city.json.bz2'),
]


def load_cities_light(apps, schema_editor):
    # Skip if the geonames data has already been imported with the management command
    if apps.get_model('cities_light', 'City').objects.exists():
        return

    for model_name, fixture in MODELS:
        model = apps.get_model('cities_light', model_name)
        foreign_keys = {field.name for field in model._meta.concrete_fields if field.is_relation}

        with bz2.open(os.path.join(FIXTURES_DIR, fixture), 'rt', encoding='utf-8') as fixture_file:
            rows = json.load(fixture_file)

        objects = []
        for row in rows:
            fields = {f'{name}_id' if name in foreign_keys else name: value for name, value in row['fields'].items()}
            objects.append(model(pk=row['pk'], **fields))
        model.objects.bulk_create(objects, batch_size=1000)

    # Explicit pks were inserted, so move the sequences past them for future imports
    with schema_editor.connection.cursor() as cursor:
        for model_name, _ in MODELS:
            table = apps.get_model('cities_light', model_name)._meta.db_table
            cursor.execute(f"SELECT setval(pg_get_serial_sequence('{table}', 'id'), COALESCE(MAX(id), 1)) FROM {table}")


class Migration(migrations.Migration):

    dependencies = [
        ('cities_light', '0013_alter_city_alternate_names_alter_city_country_and_more'),
        ('core', '0019_address'),
    ]

    operations = [
        migrations.RunPython(load_cities_light, migrations.RunPython.noop),
    ]
