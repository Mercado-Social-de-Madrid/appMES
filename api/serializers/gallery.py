from rest_framework import serializers

from core.models import Gallery, GalleryPhoto


class GalleryPhotoSerializer(serializers.ModelSerializer):
    photo = serializers.StringRelatedField(source="photo.name")

    class Meta:
        model = GalleryPhoto
        fields = ['order', 'title', 'photo', 'uploaded']


class GallerySerializer(serializers.ModelSerializer):
    photos = GalleryPhotoSerializer(many=True)

    class Meta:
        model = Gallery
        fields = ['title', 'photos']


