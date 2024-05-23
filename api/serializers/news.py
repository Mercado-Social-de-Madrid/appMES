from rest_framework import serializers

from news.models import News


class NewsSerializer(serializers.ModelSerializer):
    banner_image = serializers.StringRelatedField(source="banner_image.name")
    id = serializers.StringRelatedField()

    class Meta:
        model = News
        exclude = []
