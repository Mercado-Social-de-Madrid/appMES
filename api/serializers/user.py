from rest_framework import serializers

from authentication.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ["id", "password", "is_staff", "is_superuser"]