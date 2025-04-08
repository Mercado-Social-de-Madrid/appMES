from django.apps import apps
import logging
import os
from django.db.models.signals import post_save
from django.dispatch import receiver
from sentence_transformers import SentenceTransformer
from core.vectorize import vectorize_records

# Logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Get the embedding model from the app configuration
model = apps.get_app_config("core").embedding_model

@receiver(post_save)
def update_embedding(sender, instance, **kwargs):
    """
    Signal that is automatically executed when a record is inserted or updated in Provider.
    """
    logging.info(f"🔄 Vectorizing Provider ID {instance.pk}...")
    vectorize_records("Provider", ["short_description", "description", "services"], "embedding_desc", instance)