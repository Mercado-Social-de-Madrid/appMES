from rest_framework.serializers import BaseSerializer


class SemanticSearchSerializerMixin(BaseSerializer):

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        print("AAAAAAAA")

        if hasattr(instance, 'exact_match'):
            representation['exact_match'] = instance.exact_match

        if hasattr(instance, 'similarity'):
            representation['similarity'] = instance.similarity

        return representation