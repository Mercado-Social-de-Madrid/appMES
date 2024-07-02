
from rest_framework import serializers

from api.mixins.ExcludeTranslationFieldsMixin import ExcludeTranslationFieldsMixin
from news.models import News


class NewsSerializer(ExcludeTranslationFieldsMixin, serializers.ModelSerializer):
    banner_image = serializers.StringRelatedField(source="banner_image.name")
    id = serializers.StringRelatedField()

    class Meta:
        model = News
        exclude = []
