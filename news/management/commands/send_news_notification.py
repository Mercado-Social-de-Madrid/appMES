from authentication.models import User
from core.models import Node
from helpers import send_broadcast
from market.models import Account, Provider, Consumer
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Command to test news notifications'

    def add_arguments(self, parser):
        parser.add_argument('-t', '--topic', type=str, required=True, help='Topic')
        parser.add_argument('-m', '--message', type=str, required=False, help='Message')

    def handle(self, *args, **options):

        topic = options['topic']
        message = options['message'] or "Test notification message"

        title = "Test notification"

        send_broadcast(topic, {}, title, message, None, False)


