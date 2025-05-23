import operator
from functools import reduce
import django_filters
from django.db.models import Q
from pgvector.django import CosineDistance
from core.vectorize import clean_text
from django.apps import apps  # Para obtener el modelo de embeddings cargado en apps.py
import logging

logger = logging.getLogger(__name__)

# Obtener el modelo de embeddings cargado en apps.py (evita recargas innecesarias)
embedding_model = apps.get_app_config("core").embedding_model

class SemanticSearchFilter(django_filters.Filter):
    def __init__(self, vector_field, *args, **kwargs):
        """
        Filtro para búsqueda semántica reutilizable en cualquier modelo Django con pgvector.
        :param vector_field: Nombre del campo vectorial en la base de datos (ej. 'embedding_description').
        """
        self.vector_field = vector_field
        self.token_reducer = kwargs.pop('token_reducer', operator.and_)  # Permite combinar términos en búsqueda
        super().__init__(*args, **kwargs)

    def filter(self, qs, value):
        """
        Filtra un queryset utilizando búsqueda semántica con `pgvector`.
        """
        if value not in (None, ''):
            # Preprocesar la consulta
            query_text = clean_text(value)
            query_embedding = embedding_model.encode(query_text).tolist()

            # Aplicar búsqueda semántica con CosineDistance
            qs = qs.annotate(
                similarity=CosineDistance(self.vector_field, query_embedding)
            ).filter(
                **{f"{self.vector_field}__isnull": False}  # Excluir registros sin embeddings
            ).order_by("similarity")  # Ordenar por similitud

            # logger.info(qs.query)
            entities = qs.all()
            logger.info([f'{entity.name} - {entity.similarity}' for entity in entities])

        return qs.filter(similarity__lt=0.5)
