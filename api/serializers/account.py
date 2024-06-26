from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from market.models import Account


class AccountSerializer(serializers.ModelSerializer):
    cif = serializers.ReadOnlyField()
    email = serializers.ReadOnlyField()
    node = serializers.ReadOnlyField(source='node.pk')
    member_id = serializers.ReadOnlyField()
    owner = serializers.ReadOnlyField(source='owner.pk')
    is_active = serializers.ReadOnlyField()
    last_updated = serializers.ReadOnlyField()
    registration_date = serializers.ReadOnlyField()

    class Meta:
        model = Account
        exclude = ["polymorphic_ctype"]


class ProfileImageSerializer(serializers.ModelSerializer):
    profile_image = Base64ImageField()

    class Meta:
        model = Account
        fields = ["profile_image"]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        profile_image_url = data['profile_image']
        # Remove "/media" prefix as the mobile apps expects the path without it
        prefix = "/media"
        if profile_image_url.startswith(prefix):
            data['profile_image'] = profile_image_url.replace(prefix, "")
        return data
