from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from countries.models import Country
from .models import *


class PaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ["name", "logo"]


class PaymentGatewaySerializer(serializers.ModelSerializer):
    payment_options = serializers.SlugRelatedField(
        slug_field="name", queryset=PaymentMethod.objects.all(), many=True)
    countries = serializers.SlugRelatedField(
        slug_field="name", queryset=Country.objects.all(), many=True)

    class Meta:
        model = PaymentGateway
        fields = ["name", "payment_options", "countries", "bio",
                  "about", "accepted_methods", "target_audience", "logo", "average_rating"]

class PaymentGatewayGetSerializer(serializers.ModelSerializer):
    payment_options = PaymentMethodSerializer(many=True)
    countries = serializers.SlugRelatedField(
        slug_field="name", queryset=Country.objects.all(), many=True)

    class Meta:
        model = PaymentGateway
        fields = ["name", "payment_options", "countries", "bio",
                  "about", "accepted_methods", "target_audience", "logo", "average_rating"]


class UserRatingSerializer(serializers.ModelSerializer):
    payment_gateway = serializers.SlugRelatedField(
        slug_field="name", queryset=PaymentGateway.objects.all())

    class Meta:
        model = UserRating
        fields = "__all__"

    def create(self, validated_data):
        user = validated_data["user"]
        payment_gateway = validated_data["payment_gateway"]

        if UserRating.objects.filter(user=user, payment_gateway=payment_gateway).exists():
            raise ValidationError(
                "Users can't rate the same payment gateway more than once.")

        return UserRating.objects.create(**validated_data)


# class PaymentOptionCountrySerializer(serializers.ModelSerializer):
#     supported_countries = serializers.StringRelatedField(
#         many=True, source="country")

#     class Meta:
#         model = PaymentOption
#         fields = ['payment_option', 'supported_countries']


# class SingleCountrySerializer(serializers.ModelSerializer):region = serializers.StringRelatedField()
#     payment_options = PaymentOptionSerializer(many=True)

#     class Meta:
#         model = Country
#         fields = ["name", "capital", "region", "payment_options"]


# class AddPaymentOptionSerializer(serializers.ModelSerializer):
#     payment_option = serializers.CharField(max_length=255)
#     country = serializers.SlugRelatedField(queryset=Country.objects.all(),
#                                            slug_field="name", many=True)

#     class Meta:
#         model = PaymentOption
#         fields = ['payment_option', 'country']

#     def create(self, validated_data):
#         supported_country_names = validated_data.pop('country', [])

#         payment_option = PaymentOption.objects.create(
#             payment_option=validated_data['payment_option'])

#         for country_name in supported_country_names:
#             country = Country.objects.get(name=country_name)
#             payment_option.country.add(country)

#         return payment_option


# {
#     "payment_option": "Xsolla",
#     "country": [
#         "United States",
#         "Russia",
#         ]
# }

# {
#     "payment_option": "Square",
#     "country": [
#         "name": "United States",
#         "name": "Canada",
#         "name": "Japan",
#         "name": "Australia",
#         "name": "United Kingdom"
#         ]
# }
