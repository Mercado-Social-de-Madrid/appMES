from django.core.management.base import BaseCommand

from core.models import Node
from market.models import Provider


class Command(BaseCommand):
    help = 'Delete providers and its associated User'

    def add_arguments(self, parser):
        parser.add_argument('--node', type=int, help='Node Id')

    def handle(self, *args, **options):

        node_id = options['node']
        node = Node.objects.get(pk=node_id)

        providers = Provider.objects.filter(node=node)

        print(f'Deleting providers. Total {len(providers)}')
        current = 0

        for provider in providers:
            current += 1
            print(f'Current: {current}', end='\r')
            if provider.owner:
                provider.owner.delete()
                provider.gallery.delete()
            provider.delete()

        print("\n")