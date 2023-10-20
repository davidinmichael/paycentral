from rest_framework import serializers
from .models import *
from countries.serializers import *


class PaymentOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentOption
        fields = ["payment_option"]

class PaymentOptionCountrySerializer(serializers.ModelSerializer):
    supported_countries = serializers.StringRelatedField(many=True, source="country")
    class Meta:
        model = PaymentOption
        fields = ['payment_option', 'supported_countries']


# class AddPaymentOptionSerializer(serializers.ModelSerializer):
#     payment_option = serializers.CharField(max_length=255)
#     country = serializers.SlugRelatedField(queryset=Country.objects.all(), slug_field="name")

#     class Meta:
#         model = PaymentOption
#         fields = ['payment_option', 'country']


class SingleCountrySerializer(serializers.ModelSerializer):
    region = serializers.StringRelatedField()
    payment_options = PaymentOptionSerializer(many=True)
    class Meta:
        model = Country
        fields = ["name", "capital", "region", "payment_options"]


class AddPaymentOptionSerializer(serializers.ModelSerializer):
    payment_option = serializers.CharField(max_length=255)
    country = serializers.ListField(child=serializers.CharField(max_length=100))

    class Meta:
        model = PaymentOption
        fields = ['payment_option', 'country']

    def create(self, validated_data):
        supported_country_names = validated_data.pop('country', [])

        payment_option = PaymentOption.objects.create(payment_option=validated_data['payment_option'])

        for country_name in supported_country_names:
            country = Country.objects.get(name=country_name)
            payment_option.country.add(country)

        return payment_option


# {
#     "payment_option": "Xsolla",
#     "country": [
#         "United States",
#         "Russia",
#         ]
# }