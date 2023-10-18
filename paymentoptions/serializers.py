from rest_framework import serializers
from .models import *
from countries.serializers import *

class PaymentOptionSerializers(serializers.ModelSerializer):
    supported_countries = serializers.StringRelatedField(many=True, source="country")
    class Meta:
        model = PaymentOption
        fields = ['payment_option', 'supported_countries']


class CountryPaymentOptionSerializer(serializers.ModelSerializer):
    country = CountrySerializer(many=True)
    class Meta:
        model = PaymentOption
        fields = ["country", "payment_option"]


class AddPaymentOptionSerializer(serializers.ModelSerializer):
    payment_option = serializers.CharField(max_length=255)
    country = serializers.ListField(child=serializers.CharField(max_length=100))

    class Meta:
        model = PaymentOption
        fields = ['payment_option', 'country']

    def create(self, validated_data):
        # Extract the list of supported countries by name
        supported_country_names = validated_data.pop('country', [])
        print(type(supported_country_names))

        # Create the payment option
        payment_option = PaymentOption.objects.create(payment_option=validated_data['payment_option'])

        # Associate the payment option with the selected countries
        for country_name in supported_country_names:
            country, created = Country.objects.get_or_create(name=country_name)
            payment_option.country.add(country)

        return payment_option

