import json
import operator
from functools import reduce
import django_filters
from django.conf import settings
from django.db.models import Q, ExpressionWrapper, BooleanField
from pgvector.django import CosineDistance
from django.apps import apps  # Para obtener el modelo de embeddings cargado en apps.py
import logging

from helpers.filters.search_text_processing import clean_text

logger = logging.getLogger(__name__)

from helpers.filters.SearchFilter import SearchFilter

# Obtener el modelo de embeddings cargado en apps.py (evita recargas innecesarias)
embedding_model = apps.get_app_config("core").get_embedding_model()

class SemanticSearchFilter(SearchFilter):
    def __init__(self, vector_field='embedding_description', names=[], *args, **kwargs):
        """
        Filtro para búsqueda semántica reutilizable en cualquier modelo Django con pgvector.
        :param vector_field: Nombre del campo vectorial en la base de datos (ej. 'embedding_description').
        """
        self.vector_field = vector_field
        super().__init__(names=names, *args, **kwargs)

    def filter(self, qs, value):
        """
        Filtra un queryset utilizando búsqueda semántica con `pgvector`.
        """
        if value not in (None, ''):
            # Preprocesar la consulta
            query_text = clean_text(value)

            if settings.ENABLE_VECTOR_EMBEDDING:
                query_embedding = embedding_model.encode(query_text).tolist()
                # Aplicar búsqueda semántica con CosineDistance
                qs = qs.annotate(
                    similarity=CosineDistance(self.vector_field, query_embedding),
                    exact_match=ExpressionWrapper(reduce(operator.or_, self.get_subquery_list(value)), output_field=BooleanField())
                ).filter(Q(exact_match=True) | Q(similarity__lt=settings.SEMANTIC_SIMILARITY_THRESHOLD) | Q(similarity__isnull=True)
                ).order_by('-exact_match', 'similarity')  # Ordenar por similitud

                entities = qs.all()
                data = {
                    "original": value,
                    "procesado": query_text,
                    "resultados": [{"id": str(entity.id), "nombre": entity.name, "similitud": entity.similarity} for entity in entities]
                }
                logger.info(f'[BUSQUEDA] - {json.dumps(data)}')


            else:
                qs = super().filter(qs, value)

        return qs
