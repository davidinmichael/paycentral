from urllib import response
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from paymentoptions.models import PaymentOption
from django.db.models import Q
from paymentoptions.serializers import *
from .models import *
from .serializers import *
from bs4 import BeautifulSoup
import lxml
import requests


class Countries(APIView, PageNumberPagination):
    def get(self, request):
        countries = Country.objects.all().order_by("name")
        response = self.paginate_queryset(countries, request, view=self)
        serializer = CountrySerializer(response, many=True)
        return self.get_paginated_response(serializer.data)


class AllRegion(APIView):
    def get(self, request):
        regions = Region.objects.all().order_by("name")
        serializer = RegionSerializer(regions, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    

class SingleRegion(APIView):
    def get(self, request, pk):
        try:
            region = Region.objects.get(id=pk)
        except Region.DoesNotExist:
            return Response({"message": "Oops, no available region"})
        countries = Country.objects.filter(region=region).order_by("name")
        serializer = CountrySerializer(countries, many=True)
        if not countries:
            return Response({"message": "No country found for this region"}, status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status.HTTP_200_OK)


class CountriesAndPaymentMethods(APIView, PageNumberPagination):
    def get(self, request):
        countries = Country.objects.all().order_by("name")
        response = self.paginate_queryset(countries, request, view=self)
        serializer = SingleCountrySerializer(response, many=True)
        return self.get_paginated_response(serializer.data)


class SingleCountryAndPayment(APIView):
    def get(self, request, pk):
        data = {}
        country = Country.objects.get(id=pk)
        country_serializer = CountrySerializer(country)
        payment_option = PaymentOption.objects.filter(country=country)
        serializer = PaymentOptionSerializer(payment_option, many=True)
        data["country"] = country_serializer.data
        if payment_option:
            data["supported_payment_options"] = serializer.data
            return Response(data, status.HTTP_200_OK)
        else:
            data["supported_payment_options"] = "No supported payment method for this country yet"
            return Response(data, status.HTTP_200_OK)


class SearchCountry(APIView, PageNumberPagination):
    def get(self, request, name):
        countries = Country.objects.filter(
            Q(name__icontains=name) | Q(region__name__icontains=name) | Q(capital__icontains=name)
    ).order_by('name')
        if not countries:
            return Response({"message": "Oops, country not found, check the spelling and try again."})
        response = self.paginate_queryset(countries, request, view=self)
        serializer = SingleCountrySerializer(response, many=True)
        return self.get_paginated_response(serializer.data)

    

# Getting all countries and regions
# class Countries(APIView, PageNumberPagination):
#     def get(self, request):
#         # region_name_new = Region.objects.create(name="Others")
#         # url = "https://restcountries.com/v3.1/all"

#         # try:
#         #     response = requests.get(url)

#         #     if response.status_code == 200:
#         #         data = response.json()

#         #         for country_data in data:
#         #             country_name = country_data["name"]["common"]
#         #             capital_list = country_data.get("capital", ["N/A"])
#         #             capital = capital_list[0]

#         #             region_name = country_data.get("region", "N/A")
#         #             if region_name:
#                         # region_, _ = Region.objects.get_or_create(name=region_name)
#         #             else:
#         #                 # If region is not found, associate with the "Others" region
#                         # region_ = Region.objects.get(name="Others")

#         #             # Create a new Country instance and save it to the database
#         #             country, created = Country.objects.get_or_create(name=country_name, capital=capital, region=region)
#         #             if created:
#         #                 print(f"Created country: {country.name} (Capital: {country.capital})")

#         #             # Associate the country with the region (if a valid region is found)

#         #     else:
#         #         print("Failed to retrieve data from the API.")
#         # except requests.exceptions.RequestException as e:
#         #     print("An error occurred:", e)

#         countries = Country.objects.all().order_by("name")
#         response = self.paginate_queryset(countries, request, view=self)
#         serializer = CountrySerializer(response, many=True)
#         # return Response(serializer.data, status=status.HTTP_200_OK)
#         return self.get_paginated_response(serializer.data)