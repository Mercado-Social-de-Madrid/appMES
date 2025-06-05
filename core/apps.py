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

    _embedding_model = None

    def ready(self):

        # Solo inicializar en el servidor web, no en comandos
        import sys
        if 'runserver' in sys.argv or 'gunicorn' in sys.argv[0]:
            pass  # No cargar aquí, usar lazy loading

    @classmethod
    def get_embedding_model(cls):
        if cls._embedding_model is None:

            # Cargar el modelo solo cuando se necesite
            logging.info("🔄 Loading embedding model into memory...")
            # Load embedding model for use in CPU
            cls._embedding_model = SentenceTransformer(
                os.getenv('ST_MODEL', 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'),
                device='cpu'
            )
            logging.info(f"✅ Embedding model loaded. {cls._embedding_model}")

        return cls._embedding_model

