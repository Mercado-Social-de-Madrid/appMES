import json
from datetime import datetime

from django.core.management import BaseCommand

from authentication.models import User
from core.models import Node
from market.management.commands.import_madrid_data import DATETIME_FORMAT, set_categories, set_social_profiles, \
    set_offers, set_benefit, set_gallery
from market.models import Provider


def import_provider(item, node):

    try:
        user_created = User.objects.create(
            email=item['email'],
            first_name=item['name'],
            password=item['password'],
            node=node,
        )

        cif = item['cif']
        email = item['email']

        provider_created = Provider.objects.create(
            id=item['id'],
            node=node,
            owner=user_created,
            cif=item['cif'],
            name=item['name'],
            is_active=not item['inactive'],
            email=item['email'],
            member_id=item['member_id'],
            address=item['address'],
            phone_number=item['phone_number'],
            registration_date=datetime.strptime(item['registered'], DATETIME_FORMAT),

            description=item['description'],
            short_description=item['short_description'],
            latitude=item['latitude'],
            longitude=item['longitude'],
            legal_form=item['legal_form'],
            balance_detail=item['balance_detail'],
            not_listed=item['hidden'],
            webpage_link=item['webpage_link'],

        )

        provider_created.profile_image.name = item['logo']

        set_categories(item, provider_created)

        provider_created.save()

        set_social_profiles(item, provider_created)
        set_offers(item, provider_created)
        set_benefit(item, provider_created)
        set_gallery(item, provider_created)

    except Exception as error:
        print(f"Provider save error: {email} - {cif} - {error}.")


class Command(BaseCommand):
    help = 'Import a single provider of previous app Madrid data'

    def add_arguments(self, parser):

        parser.add_argument('-n', '--node', type=int, required=True, help='Node Id of Madrid (required)')
        parser.add_argument('--id', type=str, required=True, help='ID of Provider')

    def handle(self, *args, **options):

        node_id = options['node']
        provider_id = options['id']

        node = Node.objects.get(pk=node_id)

        with open('data/all_data.json', 'rb') as f:
            data = json.load(f)
            providers = data['providers']

            try:
                provider_data = next(provider for provider in providers if provider['id'] == provider_id)
                print(f"Provider found: {provider_data['name']}")
                import_provider(provider_data, node)
            except StopIteration:
                print(f"ID ({provider_id}) not found in all_data.json")

