from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.mail import send_mail


class Command(BaseCommand):
    help = 'Just a command to test emails are working'

    def add_arguments(self, parser):
        parser.add_argument('email_dest', type=str, help='Destination email')
        parser.add_argument('message', type=str, help='Message')

    def handle(self, *args, **options):

        email_dest = options['email_dest']
        message = options['message']

        try:
            send_mail(
                "Email prueba Mercado Social",
                message,
                settings.EMAIL_SEND_FROM,
                [email_dest],
                fail_silently=False,
            )

        except Exception as e:
            print(e)
