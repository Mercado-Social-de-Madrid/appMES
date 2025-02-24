from django.core.management.commands import makemessages

class Command(makemessages.Command):
    help = "Custom makemessages command that always includes --all --no-wrap"

    def handle(self, *args, **options):
        options["no-wrap"] = True
        options["all"] = True

        super().handle(*args, **options)