from django.core.management.base import BaseCommand

from market.models import Account


class Command(BaseCommand):
    help = 'Check duplicated account emails for all accounts of all nodes'

    def handle(self, *args, **options):

        accounts = Account.objects.all()

        print(f'Checking accounts. Total {len(accounts)}')

        emails = []

        for account in accounts:

            email = account.email
            if email in emails:
                print(f"Email duplicated: {email}. Node {account.node}")
            else:
                emails.append(email)