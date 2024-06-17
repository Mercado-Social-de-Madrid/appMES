import csv
from datetime import datetime

from django.core.management.base import BaseCommand
from market.models import Consumer
from core.models import Node
from django.db.models import Q


class Command(BaseCommand):
    help = 'Import all data of Madrid from old application'

    def add_arguments(self, parser):

        parser.add_argument('-n', '--node', type=int, required=True, help='Node Id of Aragón (required)')

    def handle(self, *args, **options):

        node_id = options['node']
        node = Node.objects.get(pk=node_id)

        with open('data/aragon_consumers.csv', 'r', encoding="utf8") as fp:
            csv_reader = csv.reader(fp, delimiter=';')
            line = 0

            for row in csv_reader:
                if line == 0:
                    line += 1
                    continue

                member_id = row[0]
                nif = row[1].replace("-", "").replace(" ", "")
                name = row[2].title()
                surnames = row[3].title()
                email = row[4].lower()
                phone = row[5]
                district_code = row[6].replace(".", "")
                city = row[7].title()
                address = row[8]
                area = row[9].capitalize()
                registration_date = row[10]
                intercoop = row[11] == "SI"

                full_address = f"{address}, {district_code}, {city}, {area}"

                existing_consumer = Consumer.objects.filter(Q(cif=nif) | Q(email=email)).first()
                if existing_consumer:
                    print(f"Consumer already exists: {email} - {nif}")
                    continue

                consumer_created = Consumer.objects.create(
                    node=node,
                    first_name=name,
                    last_name=surnames,
                    email=email,
                    cif=nif,
                    member_id=member_id,
                    address=full_address,
                    city=city,
                    phone_number=phone,
                    registration_date=datetime.strptime(registration_date, "%d/%m/%Y") if registration_date else None,
                    is_intercoop=intercoop,

                )
