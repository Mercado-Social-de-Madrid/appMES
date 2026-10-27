import re

from cities_light.abstract_models import to_ascii
from cities_light.models import SubRegion
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils.text import slugify

# Geonames names provinces as "Provincia de X" (also in ca/gl/eu/en variants). Keep only the province name.
# Patterns are case-sensitive on purpose: "Provincia de Las Palmas" or "Provincia de La Rioja" keep their article.
PATTERNS = [
    (re.compile(r"^Prov[ií]ncia de (?:las |los |la |les |l['’])?"), ''),  # es/gl/ca: "Provincia de las Islas Baleares"
    (re.compile(r"^Prov[ií]ncia d['’]?(?=[AEIOUÀÁÈÉÍÏÒÓÚ])"), ''),  # ca: "Província d'Àlaba", "Província dAlmeria"
    (re.compile(r"^Provincia da "), 'A '),  # gl: "Provincia da Coruña"
    (re.compile(r"^Provincia do "), 'O '),
    (re.compile(r"^Province of "), ''),  # en
    (re.compile(r"^Ciudad Autónoma de "), ''),  # Ceuta, Melilla
    (re.compile(r"^(.+?)(?:ko|go) probintzia$"), r'\1'),  # eu: "Almeríako probintzia"
]


def clean_name(name):
    if not name:
        return name
    for pattern, replacement in PATTERNS:
        name = pattern.sub(replacement, name)
    return name.strip()


def clean_translations(translations):
    cleaned = {}
    for lang, names in (translations or {}).items():
        # Remove the duplicates that appear when both "X" and "Provincia de X" were present
        cleaned[lang] = list(dict.fromkeys(clean_name(name) for name in names))
    return cleaned


class Command(BaseCommand):
    help = 'Removes the "Provincia de" (and equivalent) prefixes from cities_light SubRegion names and translations'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Show the changes without saving them')

    @transaction.atomic
    def handle(self, *args, **options):
        changed = 0
        for subregion in SubRegion.objects.select_related('country').order_by('name'):
            name = clean_name(subregion.name)
            translations = clean_translations(subregion.translations)
            if name == subregion.name and translations == subregion.translations:
                continue

            changed += 1
            self.stdout.write(f"{subregion.name} -> {name} {translations}")
            if options['dry_run']:
                continue

            subregion.name = name
            subregion.name_ascii = to_ascii(name).strip()
            subregion.slug = slugify(subregion.name_ascii)
            subregion.translations = translations
            subregion.save()  # The cities_light pre_save receiver recalculates display_name

        self.stdout.write(self.style.SUCCESS(f"{changed} subregions {'would be ' if options['dry_run'] else ''}updated"))
