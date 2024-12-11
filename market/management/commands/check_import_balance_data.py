import csv
from datetime import datetime

from django.core.management.base import BaseCommand
from market.models import Consumer, Provider
from core.models import Node
from django.db.models import Q


class Command(BaseCommand):
    help = 'Check CIFs and emails of balance data csv to import (run before import_balance_data command)'

    def add_arguments(self, parser):

        parser.add_argument('-n', '--node', type=int, required=True, help='Node Id')

    def handle(self, *args, **options):

        node_id = options['node']
        node = Node.objects.get(pk=node_id)

        print('Starting check import process...')

        with open('data/balance_data.csv', 'r', encoding="utf8") as fp:
            csv_reader = csv.reader(fp, delimiter=';')

            line = 0
            for row in csv_reader:
                if line == 0:
                    line += 1
                    continue

                name = row[0]
                email = row[1]
                cif = row[2]

                provider = Provider.objects.filter(node=node, cif=cif)
                if not provider:
                    self.stdout.write(self.style.WARNING(f'Entity not found: {cif} - {email} - {name}'))




