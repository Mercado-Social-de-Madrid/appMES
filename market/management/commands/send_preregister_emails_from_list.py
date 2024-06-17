import time

from django.core.management.base import BaseCommand

from authentication.models import User


class Command(BaseCommand):
    help = 'Take a list of emails of file (in data/ path) and send preregister emails to them'

    def add_arguments(self, parser):
        parser.add_argument('--filename', type=str, help='Filename of email list (each in new line), inside data/ dir')

    def handle(self, *args, **options):

        filename = options['filename']

        not_found_emails = []

        with open(f'data/{filename}', 'r') as file:
            for line in file:
                email = line.strip()
                user = User.objects.filter(email=email).first()
                if user and user.preregister:
                    print(f'Sending preregister email: {email}')
                    user.preregister.first().send_email()
                    time.sleep(2)  # to void possible errors due to very quick email sending
                else:
                    not_found_emails.append(email)
                    print(f'User or preregister not found: {email}')

        print("\nNot found user or preregister emails:")
        print("\n".join(not_found_emails))
