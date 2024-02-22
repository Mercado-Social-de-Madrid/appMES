import csv
import json
import re

import requests
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import IntegrityError

from market.models import Account, Provider
from core.models import Node
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.db.utils import DataError

from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

from market.models import Category
from core.models import Node

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