import argparse
import time

from django.core.management.base import BaseCommand

from authentication.models import User
from authentication.models.preregister import PreRegisteredUser
from core.models import Node
from market.models import Account, Consumer


class Command(BaseCommand):
    help = 'Create preregister user for all accounts of node'

    def add_arguments(self, parser):
        parser.add_argument('--node', type=int, help='Node Id')
        parser.add_argument('--intercoop', action=argparse.BooleanOptionalAction)
        parser.set_defaults(intercoop=True)

    def handle(self, *args, **options):

        node_id = options['node']
        include_intercoop = options['intercoop']

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

            if not include_intercoop and isinstance(account, Consumer) and account.is_intercoop:
                print(f"Skiping intercoop: {account.email}")
                continue

            print(f"Creating user and preregister: {account.email}")
            PreRegisteredUser.create_user_and_preregister(account)
            time.sleep(2)  # to void possible errors due to very quick email sending

        print("\nExisting emails:")
        print("\n".join(existing_emails))
