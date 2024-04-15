import json

from django.core.management.base import BaseCommand
from django.db import IntegrityError

from news.models import News
from core.models import Node
from market.models import Category, Consumer, Provider
from authentication.models import User

from datetime import datetime
from django.core.files import File
from django.db.models import Q

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"

def import_news(news, node):
    for item in news:
        news_created = News.objects.create(
            node=node,
            title=item['title'],
            description=item['description'],
            short_description=item['short_description'],
            # banner_image=File(...)item['banner_image'],
            # banner_thumbnail=File(...)item['banner_thumbnail'],
            more_info_text=item['more_info_text'],
            more_info_url=item['more_info_url'],
        )
        news_created.published_date = datetime.strptime(item['published_date'], DATETIME_FORMAT)
        news_created.banner_image.name = item['banner_image']
        news_created.banner_thumbnail.name = item['banner_thumbnail']
        news_created.save()

def import_categories(categories, node):
    for item in categories:
        Category.objects.create(
            node=node,
            id=item['id'],
            name=item['name'],
            description=item['description'],
            color=item['color'],
        )

def import_consumers(consumers, node):
    for item in consumers:

        cif = item['nif']
        email = item['email']

        if not cif or len(cif) > 30:
            print(f"Invalid consumer nif: {item['name']} - {email} - {cif}")
            continue

        existing_consumer = Consumer.objects.filter(Q(cif=cif) | Q(email=email) | Q(owner__email=email)).first()
        if existing_consumer:
            print(f"Consumer already exists: {item['email']} - {cif}")
            continue

        user_created = User.objects.create(
            email=item['email'],
            first_name=item['name'],
            last_name=item['surname'],
            password=item['password'],
            node=node,
        )

        consumer_created = Consumer.objects.create(
            id=item['id'],
            node=node,
            owner=user_created,
            first_name=item['name'],
            last_name=item['surname'],
            email=item['email'],
            is_intercoop=item['is_intercoop'],
            cif=cif,
            is_active= not item['inactive'],
            member_id=item['member_id'],
            address=item['address'],
            registration_date=datetime.strptime(item['registered'], DATETIME_FORMAT),

        )
        consumer_created.profile_image.name = item['profile_image']
        consumer_created.save()

class Command(BaseCommand):
    help = 'Import all data of Madrid from old application'

    def add_arguments(self, parser):

        parser.add_argument('--node', type=int, help='Node Id of Madrid')

    def handle(self, *args, **options):

        node_id = options['node']
        node = Node.objects.get(pk=node_id)

        with open('all_data.json', 'rb') as f:
            data = json.load(f)

            # print("Importing news, {} items".format(len(data['news'])))
            # import_news(data['news'], node)

            # print("Importing categories, {} items".format(len(data['categories'])))
            # import_categories(data['categories'], node)

            print("Importing consumers, {} items".format(len(data['consumers'])))
            import_consumers(data['consumers'], node)

        return



        entities = []
        with open(jsonfile, 'rb') as fp:
            list = json.load(fp)

            for item in list:

                try:
                    entity = Entity.objects.get(email=item['email'])
                except:
                    continue

                if 'name' in item and item['name']:
                    entity.name = item['name']

                if 'email' in item and item['email']:
                    entity.email = item['email']

                if 'address' in item and item['address']:
                    entity.address = item['address']

                if 'description' in item and item['description']:
                    entity.description = item['description']

                if 'short_description' in item and item['short_description']:
                    entity.short_description = item['short_description']

                if 'latitude' in item and item['latitude']:
                    entity.latitude = item['latitude']

                if 'longitude' in item and item['longitude']:
                    entity.longitude = item['longitude']

                if 'max_percent_payment' in item and item['max_percent_payment']:
                    entity.max_percent_payment = item['max_percent_payment']

                if 'bonus_percent_general' in item and item['bonus_percent_general']:
                    entity.bonus_percent_general = item['bonus_percent_general']

                if 'bonus_percent_entity' in item and item['bonus_percent_entity']:
                    entity.bonus_percent_entity = item['bonus_percent_entity']

                if 'facebook_link' in item and item['facebook_link']:
                    entity.facebook_link = item['facebook_link']

                if 'twitter_link' in item and item['twitter_link']:
                    entity.twitter_link = item['twitter_link']

                if 'instagram_link' in item and item['instagram_link']:
                    entity.instagram_link = item['instagram_link']

                if 'telegram_link' in item and item['telegram_link']:
                    entity.telegram_link = item['telegram_link']

                if 'webpage_link' in item and item['webpage_link']:
                    entity.webpage_link = item['webpage_link']

                entity.categories.clear()
                print(entity.name)
                for categ_name in item['categories']:
                    category = Category.objects.get(name=categ_name)
                    if not category:
                        raise Exception('category not found: ' + categ_name + ", Entity: " + entity.name)
                    entity.categories.add(category)

                entities.append(entity)

            print('Saving entities lenght: ' + str(len(entities)))
            for entity in entities:

                print('saving: ' + entity.name)
                try:
                    entity.save()
                except IntegrityError as e:
                    print(e)
                except Exception as e:
                    print(e)
