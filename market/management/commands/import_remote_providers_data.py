import requests
from django.core.management import BaseCommand

from core.models import Node
from market.models import Provider


class Command(BaseCommand):
    help = 'Import market providers data from remote api'

    def add_arguments(self, parser):

        parser.add_argument('-rn', '--remote_node', type=int, required=True, help='Remote node id')
        parser.add_argument('-ln', '--local_node', type=int, required=True, help='Local node id')

    def handle(self, *args, **options):

        remote_node_id = options['remote_node']
        local_node_id = options['local_node']

        url = f"https://mercadosocial.app/api/v2/nodes/{remote_node_id}/providers/"

        node = Node.objects.get(pk=local_node_id)
        response = requests.get(url)

        if response.status_code == 200:
            providers = response.json()
        else:
            raise Exception(f"Translation failed: {response.text}")

        for item in providers:
            provider_created = Provider.objects.create(
                id=item['id'],
                node=node,
                cif=item['cif'],
                name=item['name'],
                email=item['email'],
                member_id=item['member_id'],
                address=item['address'],
                phone_number=item['phone_number'],

                description=item['description'],
                short_description=item['short_description'],
                services=item['services'],
                latitude=item['latitude'],
                longitude=item['longitude'],
                webpage_link=item['webpage_link'],

            )