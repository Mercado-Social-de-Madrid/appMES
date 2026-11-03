import re
import unicodedata
from collections import defaultdict

from cities_light.models import City, SubRegion
from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import Address
from market.models import Account

# The first two digits of a Spanish postcode are the INE province code. Map them to the geonames codes of SubRegion.
POSTCODE_PROVINCES = {
    '01': 'VI', '02': 'AB', '03': 'A', '04': 'AL', '05': 'AV', '06': 'BA', '07': 'PM', '08': 'B', '09': 'BU',
    '10': 'CC', '11': 'CA', '12': 'CS', '13': 'CR', '14': 'CO', '15': 'C', '16': 'CU', '17': 'GI', '18': 'GR',
    '19': 'GU', '20': 'SS', '21': 'H', '22': 'HU', '23': 'J', '24': 'LE', '25': 'L', '26': 'LO', '27': 'LU',
    '28': 'M', '29': 'MA', '30': 'MU', '31': 'NA', '32': 'OR', '33': 'O', '34': 'P', '35': 'GC', '36': 'PO',
    '37': 'SA', '38': 'TF', '39': 'S', '40': 'SG', '41': 'SE', '42': 'SO', '43': 'T', '44': 'TE', '45': 'TO',
    '46': 'V', '47': 'VA', '48': 'BI', '49': 'ZA', '50': 'Z', '51': 'CE', '52': 'ME',
}

# Optional "CP", "C.P.", "C.P:" prefix followed by a valid Spanish postcode (01000-52999)
POSTCODE_RE = re.compile(r"(?:\bC\.?\s?P\.?\s*:?\s*)?\b((?:0[1-9]|[1-4]\d|5[0-2])\d{3})\b", re.IGNORECASE)
PARENTHESIS_RE = re.compile(r"\(([^)]*)\)")
SEGMENT_SEPARATOR_RE = re.compile(r"\s*(?:,|\s-\s)\s*")


def normalize(text):
    if not text:
        return ''
    text = unicodedata.normalize('NFKD', text)
    text = ''.join(c for c in text if not unicodedata.combining(c)).lower()
    return ' '.join(re.sub(r"[^a-z0-9ñ]+", ' ', text).split())


def place_names(place):
    """ All the known names of a cities_light City/SubRegion: name, ascii, alternate names and translations """
    names = {place.name, place.name_ascii}
    names.update((place.alternate_names or '').split(';'))
    for translated in (place.translations or {}).values():
        names.update(translated)
    # Bilingual names like "Donostia / San Sebastián" or "Araba / Álava"
    for name in list(names):
        if '/' in name:
            names.update(name.split('/'))
    return {normalize(name) for name in names if name and name.strip()}


def build_index(queryset):
    index = defaultdict(list)
    for place in queryset:
        for name in place_names(place):
            index[name].append(place)
    return index


class Command(BaseCommand):
    help = 'Creates the Address of each Account from the legacy old_address and old_city fields'

    def add_arguments(self, parser):
        parser.add_argument('-n', '--node', type=int, help='Only migrate the accounts of this node')
        parser.add_argument('--overwrite', action='store_true', help='Also process accounts that already have an address')
        parser.add_argument('--dry-run', action='store_true', help='Show the parsed addresses without saving them')

    def handle(self, *args, **options):
        self.cities = build_index(City.objects.select_related('subregion'))
        self.regions = build_index(SubRegion.objects.all())
        self.regions_by_code = {region.geoname_code: region for region in SubRegion.objects.all()}

        accounts = Account.objects.non_polymorphic().select_related('address')
        accounts = accounts.exclude(old_address__isnull=True, old_city__isnull=True)
        if options['node']:
            accounts = accounts.filter(node_id=options['node'])
        if not options['overwrite']:
            accounts = accounts.filter(address__isnull=True)

        stats = defaultdict(int)
        unmatched = []
        with transaction.atomic():
            for account in accounts.order_by('node_id', 'member_id'):
                parsed = self.parse(account.old_address, account.old_city)
                if not any(parsed.values()):
                    stats['empty'] += 1
                    continue

                stats['city' if parsed['city'] else 'region' if parsed['region'] else 'no_location'] += 1
                if not parsed['city']:
                    unmatched.append(f"  [{account.pk}] address: {account.old_address!r} city: {account.old_city!r}")

                if options['dry_run'] or options['verbosity'] > 1:
                    self.stdout.write(f"{account.old_address!r} | {account.old_city!r}  ->  {self.describe(parsed)}")
                if options['dry_run']:
                    continue

                if account.address:
                    for field, value in parsed.items():
                        setattr(account.address, field, value)
                    account.address.save()
                else:
                    account.address = Address.objects.create(**parsed)
                    account.save(update_fields=['address'])

        if unmatched:
            self.stdout.write(self.style.WARNING(f"Accounts without a matching city ({len(unmatched)}):"))
            self.stdout.write('\n'.join(unmatched))

        self.stdout.write(self.style.SUCCESS(
            f"{'[DRY RUN] ' if options['dry_run'] else ''}"
            f"With city: {stats['city']}, only province: {stats['region']}, "
            f"without location: {stats['no_location']}, empty (skipped): {stats['empty']}"
        ))

    def parse(self, old_address, old_city):
        address = (old_address or '').strip()

        # Keep the last postcode, as house numbers appear before it
        postcode = None
        postcode_matches = list(POSTCODE_RE.finditer(address))
        if postcode_matches:
            match = postcode_matches[-1]
            postcode = match.group(1)
            address = address[:match.start()] + ', ' + address[match.end():]
        else:
            city_postcode = POSTCODE_RE.search(old_city or '')
            if city_postcode:
                postcode = city_postcode.group(1)
                old_city = old_city[:city_postcode.start()] + old_city[city_postcode.end():]

        postcode_region = self.regions_by_code.get(POSTCODE_PROVINCES.get(postcode[:2])) if postcode else None

        city_text, region_hints = self.split_city(old_city)
        if not city_text:
            # Without old_city, the city is usually the last part of the address: "C/ Mayor 1, 28001 Madrid"
            segments = [s for s in SEGMENT_SEPARATOR_RE.split(address) if s.strip()]
            if len(segments) > 1:
                city_text, region_hints = self.split_city(segments[-1])

        region = postcode_region or self.find_region(region_hints)
        city = self.find_city(city_text, region)
        if city:
            region = city.subregion
        elif not region:
            # Sometimes the province was written as the city
            region = self.find_region([city_text])

        return {
            'address': self.clean_address(address, city, region) or None,
            'postcode': postcode,
            'city': city,
            'region': region,
        }

    @staticmethod
    def split_city(old_city):
        """ "Alcalá de Henares (Madrid)" or "Getafe, Madrid" -> ("Alcalá de Henares", ["Madrid"]) """
        if not old_city or not old_city.strip():
            return '', []
        hints = PARENTHESIS_RE.findall(old_city)
        parts = [p for p in SEGMENT_SEPARATOR_RE.split(PARENTHESIS_RE.sub('', old_city)) if p.strip()]
        if not parts:
            return '', hints
        return parts[0].strip(), parts[1:] + hints

    def find_region(self, texts):
        for text in texts:
            regions = self.regions.get(normalize(text))
            if regions:
                return regions[0]
        return None

    def find_city(self, text, region=None):
        candidates = list({c.pk: c for c in self.cities.get(normalize(text), [])}.values())
        if not candidates:
            return None
        if region:
            in_region = [c for c in candidates if c.subregion_id == region.pk]
            if in_region:
                candidates = in_region
            else:
                self.stderr.write(self.style.WARNING(f"'{text}' is not in province {region.name}"))
        return max(candidates, key=lambda c: c.population or 0)

    def clean_address(self, address, city, region):
        """ Removes the trailing city / province names and leftover separators from the address """
        known_names = (place_names(city) if city else set()) | (place_names(region) if region else set())
        address = PARENTHESIS_RE.sub(lambda m: '' if normalize(m.group(1)) in known_names else m.group(0), address)
        # Split keeping the separators: [segment, separator, segment, ...]
        parts = re.split(f"({SEGMENT_SEPARATOR_RE.pattern})", address)
        while parts and (not parts[-1].strip() or normalize(parts[-1]) in known_names):
            parts = parts[:-2]
        # Collapse the empty segments left by the removed postcode: "C/ Mayor 1, , Bajo"
        return re.sub(r"(\s*,)(\s*,)+", r"\1", ''.join(parts)).strip(' ,-')

    @staticmethod
    def describe(parsed):
        return ' | '.join(str(parsed[key] or '-') for key in ('address', 'postcode', 'city', 'region'))
