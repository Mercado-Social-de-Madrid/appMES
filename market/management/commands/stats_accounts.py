import argparse

from django.core.management.base import BaseCommand

from authentication.models.preregister import PreRegisteredUser
from core.models import Node
from market.models import Account


class Command(BaseCommand):
    help = 'Show count (optionaly detail) of accounts, users, and preregisters'

    def add_arguments(self, parser):
        parser.add_argument('-n', '--node', type=int, required=True, help='Node Id (required)')
        parser.add_argument('-d', '--detail', action=argparse.BooleanOptionalAction)
        parser.set_defaults(detail=False)

    def handle(self, *args, **options):

        node_id = options['node']
        detail = options['detail']

        node = Node.objects.get(pk=node_id)

        accounts = Account.objects.filter(node=node)
        print(f'\nAccounts: {accounts.count()}')
        if detail:
            print([account.email for account in accounts])

        accounts_with_users = accounts.filter(owner__isnull=False)
        print(f'\nAccounts with users: {accounts_with_users.count()}')
        if detail:
            print([account.email for account in accounts_with_users])

        accounts_without_users = accounts.filter(owner__isnull=True)
        print(f'\nAccounts without users: {accounts_without_users.count()}')
        if detail:
            print([account.email for account in accounts_without_users])

        preregisters = PreRegisteredUser.objects.filter(account__node=node)
        print(f'\nPreregisters: {preregisters.count()}')
        if detail:
            print([preregister.user.email for preregister in preregisters])

        no_mail_preregisters = preregisters.filter(email_sent=False)
        print(f'\nPreregisters with no sent email: {no_mail_preregisters.count()}')
        if detail:
            print([no_mail_preregister.user.email for no_mail_preregister in no_mail_preregisters])

        print()
