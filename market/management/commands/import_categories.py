import json

from django.core.management.base import BaseCommand

from core.models import Node
from market.models import Category


class Command(BaseCommand):
    help = 'Import categories'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Indicates the Json file to import fields from')

    def handle(self, *args, **options):

        file = options['json_file']

        with open(file, 'r', encoding="utf8") as fp:
            categories = json.loads(fp.read())

            for category in categories:
                node = Node.objects.get(pk=category['node'])
                Category.objects.create(
                    node=node,
                    name=category['name'],
                    description=category['description'],
                    color=category['color'],)

            print("Categories imported")