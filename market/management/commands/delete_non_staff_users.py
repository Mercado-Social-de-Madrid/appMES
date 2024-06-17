from django.core.management.base import BaseCommand

from authentication.models import User
from core.models import Node


class Command(BaseCommand):
    help = 'Delete non staff users'

    def add_arguments(self, parser):
        parser.add_argument('-n', '--node', type=int, required=True, help='Node Id (required)')

    def handle(self, *args, **options):

        node_id = options['node']
        node = Node.objects.get(pk=node_id)

        users = User.objects.filter(node=node, is_staff=False, is_superuser=False)

        print(f'Deleting users. Total {len(users)}')
        current = 0

        for user in users:

            current += 1
            print(f'Current: {current}', end='\r')

            user.delete()

        print("\n")