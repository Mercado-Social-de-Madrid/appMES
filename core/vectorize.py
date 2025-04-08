# vectorize.py - Functions for vectorizing text in Django
# Contains reusable methods for cleaning up text and generating embeddings.

import logging
import re
from sentence_transformers import SentenceTransformer
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords

from django.apps import apps

# Logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Download stopwords if not available
nltk.download("stopwords")
STOPWORDS_ES = set(stopwords.words("spanish"))

# Get the embedding model from the app configuration
embedding_model = apps.get_app_config("core").embedding_model

def clean_text(text):
    """Cleans text by removing HTML, URLs, special characters, and normalizing spaces."""
    if not text:
        return ""

    text = BeautifulSoup(text, "html.parser").get_text(separator=" ")
    text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)
    text = re.sub(r"[^a-zA-Z0-9áéíóúüñÁÉÍÓÚÜÑ.,;!?()'\"\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    text = text.lower()
    tokens = text.split()
    tokens = [word for word in tokens if word not in STOPWORDS_ES]
    return " ".join(tokens)

def vectorize_records(model_name, text_fields, vector_field, instance=None):
    """
    Vectorizes records from any model.
    :param model_name: Name of the Django model.
    :param text_fields: List of text fields to use.
    :param vector_field: Name of the field to save the embedding.
    :param instance: Specific instance if you want to update only one record.
    """

    model_class = apps.get_model("core", model_name)  # Get model dynamically

    logging.info(f"🔄 Vectorizing data in {model_name}...")

    if instance:
        instances = [instance]  # If an instance is provided, only process that one
    else:
        instances = model_class.objects.all()  # Bulk processing

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
        obj.save()

    logging.info(f"✅ Vectorization completed in {model_name}.")
