from rest_framework.serializers import BaseSerializer

from core.templatetags.similarity_check import similarity_level


class SemanticSearchSerializerMixin(BaseSerializer):

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if hasattr(instance, 'exact_match'):
            representation['exact_match'] = instance.exact_match

        if hasattr(instance, 'similarity'):
            representation['similarity'] = instance.similarity
            representation['similarity_level'] = similarity_level(instance.similarity)

        return representation