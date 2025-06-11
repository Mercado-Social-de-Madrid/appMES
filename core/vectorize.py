# vectorize.py - Functions for vectorizing text in Django
# Contains reusable methods for cleaning up text and generating embeddings.

import logging

from django.conf import settings
from sentence_transformers import SentenceTransformer
from bs4 import BeautifulSoup

from django.apps import apps

from helpers.filters.search_text_processing import clean_text

# Logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Get the embedding model from the app configuration
embedding_model = apps.get_app_config("core").get_embedding_model()

def vectorize_records(app_name, model_name, text_fields, vector_field, node=None, instance=None, save=True):
    """
    Vectorizes records from any model.
    :param model_name: Name of the Django model.
    :param text_fields: List of text fields to use.
    :param vector_field: Name of the field to save the embedding.
    :param node: Only vectorize records of specific node. Optional
    :param instance: Specific instance if you want to update only one record.
    :param save: Save the object after vectorization.
    """

    if not settings.ENABLE_VECTOR_EMBEDDING:
        return

    model_class = apps.get_model(app_name, model_name)  # Get model dynamically

    logging.info(f"🔄 Vectorizing data in {model_name}...")

    if instance:
        instances = [instance]  # If an instance is provided, only process that one
    else:
        # Bulk processing
        if node:
            instances = model_class.objects.filter(node=node)
        else:
            instances = model_class.objects.all()

    for obj in instances:
        # Concatenate and clean the texts
        text_parts = [clean_text(getattr(obj, field, "")) for field in text_fields]
        text = " ".join(filter(None, text_parts)).strip()

        if not text:
            logging.info(f"⚠️ Skipping {model_name} ID {obj.pk}: empty text after preprocessing.")
            continue

        # Generate embedding
        embedding = embedding_model.encode(text).tolist()

        # Save in the vector field
        setattr(obj, vector_field, embedding)

        if save:
            obj.save()

    logging.info(f"✅ Vectorization completed in {model_name}.")
