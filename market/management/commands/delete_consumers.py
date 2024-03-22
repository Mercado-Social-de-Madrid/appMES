from authentication.models import User
from market.models import Account, Provider, Consumer
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Delete consumers and its associated User'

    def handle(self, *args, **options):

        consumers = Consumer.objects.all()
        print("Found {} consumers".format(len(consumers)))
        for consumer in consumers:
            if consumer.owner:
                consumer.owner.delete()
            consumer.delete()
