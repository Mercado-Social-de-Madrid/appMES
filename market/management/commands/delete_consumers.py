from authentication.models import User
from core.models import Node
from market.models import Account, Provider, Consumer
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Delete consumers and its associated User'

    def add_arguments(self, parser):
        parser.add_argument('-n', '--node', type=int, required=True, help='Node Id (required)')

    def handle(self, *args, **options):

        node_id = options['node']
        node = Node.objects.get(pk=node_id)

        consumers = Consumer.objects.filter(node=node)

        print(f'Deleting consumers. Total {len(consumers)}')
        current = 0

        for consumer in consumers:
            current += 1
            print(f'Current: {current}', end='\r')
            if consumer.owner:
                consumer.owner.delete()
            consumer.delete()

        print("\n")