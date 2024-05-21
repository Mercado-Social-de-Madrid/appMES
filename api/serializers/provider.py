from rest_framework import serializers

from api.serializers.benefits import BenefitsSerializer
from api.serializers.category import CategorySerializer
from api.serializers.gallery import GallerySerializer
from api.serializers.offers import OffersSerializer
from api.serializers.social_profile import SocialProfileSerializer
from market.models import Provider


class ProviderSerializer(serializers.ModelSerializer):
    profile_image = serializers.StringRelatedField(source="profile_image.name")
    social_profiles = SocialProfileSerializer(many=True, read_only=True)
    gallery = GallerySerializer(many=False, read_only=True)
    offers = OffersSerializer(many=True, read_only=True)
    benefit = BenefitsSerializer(many=False, read_only=True)
    balance_url = serializers.StringRelatedField()
    categories = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = Provider
        exclude = []
