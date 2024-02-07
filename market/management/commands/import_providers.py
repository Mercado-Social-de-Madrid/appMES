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

class Command(BaseCommand):
    help = 'Import providers from CSV (first row defines field names)'

    def add_arguments(self, parser):
        parser.add_argument('csvfile', type=str, help='Indicates the CSV file to import fields from (first column must be cif)')
        parser.add_argument('region', type=str, help='Territory of market (Comunidad autónoma)')
        parser.add_argument('node_shortname', type=str, help='Shortname of node in this application')

    def handle(self, *args, **options):

        csvfile = options['csvfile']
        region = options['region']
        node_shortname = options['node_shortname']

        try:
            node = Node.objects.get(shortname=node_shortname)
        except ObjectDoesNotExist:
            print(f"Node shortname not found: {node_shortname}")
            return

        with open(csvfile, 'r', encoding="utf8") as fp:
            csv_reader = csv.reader(fp, delimiter=';')
            line = 0

            ok = 0

            for row in csv_reader:
                if line == 0:
                    line += 1
                    continue

                row_region = row[11]
                if row_region != region:
                    continue

                print("\n")
                print(row[2])

                cif = row[0]

                if not cif:
                    continue

                account = Account.objects.filter(cif=cif)
                if account.exists():
                    print("Ya existe socia con cif {}.".format(cif))
                    continue

                name = row[2]
                description = row[3]
                web = row[4]
                address = f"{row[6]}, {row[5]}, {row[14]}, {row[12]}"
                email = row[9]

                geolocator = Nominatim(user_agent="aslkj23ñl4lkfj34")

                try:
                    location = geolocator.geocode(address)
                    ok += 1
                except:
                    location = None

                try:
                    Provider.objects.create(
                        cif=cif,
                        node=node,
                        name=name,
                        description=description,
                        webpage_link=web,
                        email=email,
                        address=address,
                        latitude=location.latitude if location and location.latitude else 0,
                        longitude=location.longitude if location and location.longitude else 0,
                    )
                except DataError as e:
                    print(f"Data too long\n{cif}\n{name}\n{web}\n{email}\n{address}")

            print(f"\nSuccess locations: {ok}")