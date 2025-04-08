# apps.py - Configuration of the Core application in Django
# Loads and keeps the embedding model in memory to optimize its use.

from django.apps import AppConfig
import os
import logging
from sentence_transformers import SentenceTransformer

global embedding_model

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        
        logging.info("🔄 Loading embedding model into memory...")
        # Load embedding model for use in CPU
        self.embedding_model = SentenceTransformer(
            os.getenv('ST_MODEL', 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'),
            device='cpu'
        )
        logging.info("✅ Embedding model loaded.")
        
        # Import signals when the app starts
        import core.signals