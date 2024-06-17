import argparse
import time

from django.core.management.base import BaseCommand

from authentication.models.preregister import PreRegisteredUser
from core.models import Node


class Command(BaseCommand):
    help = 'Send welcome emails to accounts of node with pending preregister'

    def add_arguments(self, parser):
        parser.add_argument('-n', '--node', type=int, required=True, help='Node Id (required)')
        parser.add_argument('--onlycheck', action=argparse.BooleanOptionalAction)

    def handle(self, *args, **options):

        node_id = options['node']
        only_check = options['onlycheck']
        node = Node.objects.get(pk=node_id)

        preregisters = PreRegisteredUser.objects.filter(account__isnull=False, account__node=node)
        print(f'Sending emails. Preregisters count: {len(preregisters)}')
        current = 0
        for preregister in preregisters:
            current += 1
            print(f'Current: {current}. {preregister.account.display_name}')
            if not only_check:
                preregister.send_email()
                time.sleep(2)  # to void possible errors due to very quick email sending

