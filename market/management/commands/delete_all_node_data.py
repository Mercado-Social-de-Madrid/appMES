from django.core.management.base import BaseCommand

from authentication.models import User
from core.models import Node
from market.models import Provider, Consumer, Category
from news.models import News


class Command(BaseCommand):
    help = 'Delete consumers and its associated User'

    def add_arguments(self, parser):
        parser.add_argument('--node', type=int, help='Node Id')

    def handle(self, *args, **options):

        node_id = options['node']
        node = Node.objects.get(pk=node_id)

        consumers = Consumer.objects.filter(node=node)
        print(f'Deleting consumers. Total {len(consumers)}')
        current = 0
        for consumer in consumers:
            current += 1
            print(f'Current: {current}', end='\r')
            if consumer.owner:
                consumer.owner.delete()
            consumer.delete()

        providers = Provider.objects.filter(node=node)
        print(f'Deleting providers. Total {len(providers)}')
        current = 0
        for provider in providers:
            current += 1
            print(f'Current: {current}', end='\r')
            if provider.owner:
                provider.owner.delete()
            if provider.gallery:
                provider.gallery.delete()
            provider.delete()

        users = User.objects.filter(node=node, is_staff=False, is_superuser=False)
        print(f'Deleting users. Total {len(users)}')
        current = 0
        for user in users:
            current += 1
            print(f'Current: {current}', end='\r')
            user.delete()

        categories = Category.objects.filter(node=node)
        print(f'Deleting categories. Total {len(categories)}')
        current = 0
        for category in categories:
            current += 1
            print(f'Current: {current}', end='\r')
            category.delete()

        news_list = News.objects.filter(node=node)
        print(f'Deleting news. Total {len(news_list)}')
        current = 0
        for news in news_list:
            current += 1
            print(f'Current: {current}', end='\r')
            news.delete()

        print("\n")