import logging
import re
from django.apps import apps
from pgvector.django import CosineDistance
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords

# Logging configuration
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Download stopwords if not available
nltk.download("stopwords")
STOPWORDS_ES = set(stopwords.words("spanish"))

# Get the embedding model loaded in `apps.py`
embedding_model = apps.get_app_config("core").get_embedding_model()

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

def search_entities(query_text, model_name, search_fields, vector_field, limit=5):
    """
    Performs a general semantic search on any model.
    
    :param query_text: Search text entered by the user.
    :param model_name: Name of the Django model to search in.
    :param search_fields: List of fields to perform `ILIKE` search.
    :param vector_field: Field where the embeddings (`VectorField`) are stored.
    :param limit: Maximum number of results to return.
    :return: List of found objects.
    """
    
    model_class = apps.get_model("core", model_name)  # Get model dynamically
    query_text = clean_text(query_text)  # Preprocess text
    query_embedding = embedding_model.encode(query_text).tolist()  # Generate embedding

    # --- Traditional search with ILIKE ---
    traditional_results = model_class.objects.none()
    if search_fields:
        from django.db.models import Q
        q_objects = Q()
        for field in search_fields:
            q_objects |= Q(**{f"{field}__icontains": query_text})
        traditional_results = model_class.objects.filter(q_objects)

    # --- Semantic search with pgvector ---
    semantic_results = model_class.objects.annotate(
        similarity=CosineDistance(vector_field, query_embedding)
    ).order_by("similarity")[:limit]

    # --- Combine results and sort by relevance ---
    combined_results = list(traditional_results) + list(semantic_results)
    return sorted(combined_results, key=lambda x: getattr(x, "similarity", 1))