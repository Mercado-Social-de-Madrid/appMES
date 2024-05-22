from authentication.models import User
from core.models import Node
from market.models import Account, Provider, Consumer
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Delete consumers and its associated User'

    def add_arguments(self, parser):
        parser.add_argument('--node', type=int, help='Node Id')

    def handle(self, *args, **options):

        node_id = options['node']
        node = Node.objects.get(pk=node_id)

        accounts = Account.objects.filter(node=node).order_by("registration_date")

        print(f'Generating accounts member ids. Total {len(accounts)}')
        current = 0

        id = 0
        id_intercoop = 0

        for account in accounts:
            current += 1
            print(f'Current: {current}', end='\r')

            if isinstance(account, Consumer) and account.is_intercoop:
                id_intercoop += 1
                account.member_id = "ICOOP-{:05d}".format(id_intercoop)
                account.save()
            else:
                id += 1
                account.member_id = "{:05d}".format(id)
                account.save()


        print("\n")