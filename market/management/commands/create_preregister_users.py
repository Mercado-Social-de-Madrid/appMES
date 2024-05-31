import argparse
import time

from django.core.management.base import BaseCommand

from authentication.models import User
from authentication.models.preregister import PreRegisteredUser
from core.models import Node
from market.models import Account, Consumer


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

        accounts = Account.objects.filter(node=node)

        print(f'Generating users and preregisters. Total {len(accounts)}')
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

            if intercoop is None:
                print(f"Creating user and preregister: {account.email}")
                create_preregister(account)
            elif intercoop is True and account.is_intercoop:
                print(f"Creating Intercoop user and preregister: {account.email}")
                create_preregister(account)
            elif intercoop is False and not account.is_intercoop:
                print(f"Creating not Intercoop user and preregister: {account.email}")
                create_preregister(account)

        print("\nExisting emails:")
        print("\n".join(existing_emails))
