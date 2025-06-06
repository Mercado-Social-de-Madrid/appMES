# apps.py - Configuration of the Core application in Django
# Loads and keeps the embedding model in memory to optimize its use.

from django.apps import AppConfig
import os
import logging

from django.conf import settings
from sentence_transformers import SentenceTransformer
import threading

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    _model_lock = threading.Lock()
    _embedding_model = None
    _model_loaded = False

    def ready(self):

        # Solo cargar en el proceso principal del servidor
        import sys
        if any(cmd in sys.argv for cmd in ['runserver', 'gunicorn']):
            self._load_model_if_needed()

    def _load_model_if_needed(self):

        if not settings.ENABLE_VECTOR_EMBEDDING:
            return

        logging.info(f">> checking model loaded flag: {self._model_loaded}")
        if not self._model_loaded:  # Verificación rápida sin lock
            with self._model_lock:
                logging.info(f">> checking model loaded: {self._embedding_model}")
                if not self._embedding_model:
                    # Cargar el modelo solo cuando se necesite
                    logging.info("🔄 Loading embedding model into memory...")
                    # Load embedding model for use in CPU
                    self._embedding_model = SentenceTransformer(
                        os.getenv('ST_MODEL', 'sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'),
                        device='cpu'
                    )
                    logging.info(f"✅ Embedding model loaded. {self._embedding_model}")
                    self._model_loaded = True

    def get_embedding_model(self):
        self._load_model_if_needed()
        return self._embedding_model

