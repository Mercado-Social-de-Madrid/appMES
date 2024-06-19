from django.core.management.base import BaseCommand

from core.models import Node
from market.models import Account


class Command(BaseCommand):
    help = 'Check duplicated member ids for all accounts of a node'

    def add_arguments(self, parser):
        parser.add_argument('-n', '--node', type=int, required=True, help='Node Id (required)')

    def handle(self, *args, **options):

        node_id = options['node']
        node = Node.objects.get(pk=node_id)

        accounts = Account.objects.filter(node=node)

        print(f'Checking accounts. Total {len(accounts)}')

        member_ids = []

        for account in accounts:

            member_id = account.member_id
            if member_id in member_ids:
                print(f"Member id duplicated: {member_id} - {account.display_name} - {account.email}")
            else:
                member_ids.append(member_id)
                