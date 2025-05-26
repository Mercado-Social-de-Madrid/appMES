from django.apps import apps
import logging
import os
from django.db.models.signals import pre_save
from django.dispatch import receiver
from sentence_transformers import SentenceTransformer
from core.vectorize import vectorize_records
from market.models import Provider

# Logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

@receiver(pre_save, sender=Provider)
def update_embedding(sender, instance, **kwargs):
    """
    Signal that is automatically executed when a record is inserted or updated in Provider.
    """
    logging.info(f"🔄 Vectorizing Provider ID {instance.pk}...")
    vectorize_records("market",
                      "Provider",
                      ["name", "services"],
                      "embedding_description",
                      instance,
                      False)