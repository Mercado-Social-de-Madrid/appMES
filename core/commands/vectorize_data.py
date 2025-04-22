# vectorize_data.py - Command to vectorize data manually
# To run the vectorization of any model from the terminal.

from django.core.management.base import BaseCommand
from core.vectorize import vectorize_records

class Command(BaseCommand):
    help = "Vectorize data from any table."

    def add_arguments(self, parser):
        parser.add_argument("model", type=str, help="Name of the model to vectorize (e.g., Provider)")
        parser.add_argument("app", type=str, help="Name of the app to which model belongs (e.g., market)")
        parser.add_argument("text_fields", nargs="+", type=str, help="List of text fields (e.g., description short_description)")
        parser.add_argument("vector_field", type=str, help="Field to save the embedding (e.g., embedding_desc)")

    def handle(self, *args, **options):
        model_name = options["model"]
        app = options["app"]
        text_fields = options["text_fields"]
        vector_field = options["vector_field"]

        vectorize_records(app, model_name, text_fields, vector_field)
        self.stdout.write(self.style.SUCCESS(f"✅ Vectorization completed in {model_name}."))
