import argparse
import time

from django.core.management.base import BaseCommand
from django.db.models import Q

from authentication.models import User
from authentication.models.preregister import PreRegisteredUser
from core.models import Node
from market.models import Account, Consumer, Provider


def create_preregister(account):
    PreRegisteredUser.create_user_and_preregister(account)
    time.sleep(2)  # to void possible errors due to very quick email sending


class Command(BaseCommand):
    help = 'Create preregister user for all accounts of node'

    def add_arguments(self, parser):
        parser.add_argument('--node', type=int, help='Node Id')
        parser.add_argument('--intercoop', action=argparse.BooleanOptionalAction)

    def handle(self, *args, **options):

        node_id = options['node']
        intercoop = options['intercoop']

        node = Node.objects.get(pk=node_id)

        print(intercoop)
        print(type(intercoop))

        accounts = None
        if intercoop is None:
            accounts = Account.objects.filter(node=node)
        elif intercoop is True:
            accounts = Consumer.objects.filter(node=node, is_intercoop=True)
        elif intercoop is False:
            providers = Provider.objects.filter(node=node)
            consumers_no_intercoop = Consumer.objects.filter(node=node, is_intercoop=False)
            accounts = list(providers) + list(consumers_no_intercoop)

        print(f'Generating users and preregisters. Total {len(accounts)}')
        print(accounts)

        current = 0

        existing_emails = []

        for account in accounts:
            current += 1
            print(f'Current: {current}')

            # Check user email
            user = User.objects.filter(email=account.email).first()
            if user:
                print(f"User email already exists: {account.email}")
                existing_emails.append(account.email)
                continue

            print(f"Creating user and preregister: {account.email}")
            create_preregister(account)

        print("\nExisting emails:")
        print("\n".join(existing_emails))
