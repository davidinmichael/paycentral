from rest_framework import serializers
from .models import *

class PaymentOptionSerializers(serializers.ModelSerializer):
    country_names = serializers.StringRelatedField(many=True, source="country")
    class Meta:
        model = PaymentOption
        fields = ['payment_option', 'country_names']

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["name"]