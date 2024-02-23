from rest_framework import serializers

from benefits.models import Benefit


class BenefitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Benefit
        exclude = []


