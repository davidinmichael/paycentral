from rest_framework import serializers
from .models import *

class PaymentOptionSerializers(serializers.ModelSerializer):
    class Meta:
        model = PaymentOption
        fields = "__all__"

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["name"]