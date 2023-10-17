from rest_framework import serializers
from .models import *

class PaymentOptionSerializers(serializers.ModelSerializer):
    supported_countries = serializers.StringRelatedField(many=True, source="country")
    class Meta:
        model = PaymentOption
        fields = ['payment_option', 'supported_countries']

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryWiki
        fields = ["name"]