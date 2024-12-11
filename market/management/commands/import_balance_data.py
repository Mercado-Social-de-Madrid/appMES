import csv
from datetime import datetime

from django.core.management.base import BaseCommand
from weasyprint.css.validation.properties import continue_

from market.models import Consumer, Provider
from core.models import Node
from django.db.models import Q


def find_public_balance_link(csv_reader, provider_cif):
    line = 0
    for row in csv_reader:
        if line == 0:
            line += 1
            continue

        cif = row[2]
        link = row[3]
        is_public = row[5] == 'True'

        if cif == provider_cif:
            print(f'Entity found: {cif}. Is public: {is_public}')
            if is_public:
                return link

    return None


class Command(BaseCommand):
    help = 'Import all balance data to node entities. (Before running this command, run check_import_balance_data)'

    def add_arguments(self, parser):

        parser.add_argument('-n', '--node', type=int, required=True, help='Node Id')

    def handle(self, *args, **options):

        node_id = options['node']
        node = Node.objects.get(pk=node_id)
        providers = Provider.objects.filter(node=node)

        print(f'Start balance import of {len(providers)} providers...\n')

        with open('data/balance_data.csv', 'r', encoding="utf8") as fp:
            csv_reader = csv.reader(fp, delimiter=';')

            data_list = list(csv_reader)

            for provider in providers:
                balance_link = find_public_balance_link(data_list, provider.cif)
                provider.balance_detail = balance_link
                provider.save()

        print('\nImport process finished')