import json

from django.core.management.base import BaseCommand
from django.db.models import Q

from core.models import Node
from market.management.commands.import_madrid_data import set_social_profiles
from market.models import Provider, Category


def import_categories(categories, node):
    for item in categories:
        Category.objects.create(
            node=node,
            name=item['name'],
            description=item['description'],
            color=item['color'],
        )


def import_providers(providers, node):

    current = 0
    invalid = 0
    duplicated = 0
    cif_duplicated = 0
    save_errors = 0

    for item in providers:

        current += 1
        print(f'Current: {current}', end='\r')

        if item['inactive'] or item['email'] == 'etics@mercadosocial.net':
            continue

        email = item['email']

        if not email:
            print(f"Invalid provider email: {item['name']} - {email}. SKIPPING...")
            invalid += 1
            continue

        existing_provider = Provider.objects.filter(Q(email=email) | Q(owner__email=email)).first()
        if existing_provider:
            duplicated += 1
            print(f"Provider already exists: {item['email']}. SKIPPING...")
            continue

        try:

            phone_number = item['phone_number']
            if len(phone_number) > 25:
                phone_number = phone_number.split("/")[0].replace(" ", "")
                try:
                    int(phone_number)
                except:
                    print(f"Invalid phone number: {phone_number}. Original: {item['phone_number']}")
                    phone_number = None

            provider_created = Provider.objects.create(
                node=node,
                name=item['name'],
                is_active= not item['inactive'],
                email=item['email'],
                address=item['address'],
                phone_number=phone_number,
                description=item['description'],
                short_description=item['short_description'],
                latitude=item['latitude'],
                longitude=item['longitude'],
                not_listed=item['hidden'],
                webpage_link=item['webpage_link'],

            )

            provider_created.save()
            set_social_profiles(item, provider_created)

        except Exception as error:
            save_errors += 1
            print(f"Provider save error: {email} - {error}. Current: {current}")

    print(f'Invalid: {invalid}, duplicated email: {duplicated}, duplicated CIF: {cif_duplicated}, save_errors: {save_errors}')


class Command(BaseCommand):
    help = 'Import all data of Madrid from old application'

    def add_arguments(self, parser):

        parser.add_argument('--node', type=int, help='Node Id of Madrid')

    def handle(self, *args, **options):

        node_id = options['node']
        node = Node.objects.get(pk=node_id)

        with open('data/murcia_data.json', 'rb') as f:
            data = json.load(f)

            print("Importing categories, {} items".format(len(data['categories'])))
            import_categories(data['categories'], node)

            print("Importing providers, {} items".format(len(data['entities'])))
            import_providers(data['entities'], node)

