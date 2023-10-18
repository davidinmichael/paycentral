from urllib import response
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination

from paymentoptions.models import PaymentOption
from paymentoptions.serializers import CountryPaymentOptionSerializer
from .models import *
from .serializers import *
from bs4 import BeautifulSoup
import lxml
import requests


class Countries(APIView, PageNumberPagination):
    def get(self, request):
        # region_name_new = Region.objects.create(name="Others")
        # url = "https://restcountries.com/v3.1/all"

        # try:
        #     response = requests.get(url)

        #     if response.status_code == 200:
        #         data = response.json()

        #         for country_data in data:
        #             country_name = country_data["name"]["common"]
        #             capital_list = country_data.get("capital", ["N/A"])
        #             capital = capital_list[0]

        #             region_name = country_data.get("region", "N/A")
        #             if region_name:
                        # region_, _ = Region.objects.get_or_create(name=region_name)
        #             else:
        #                 # If region is not found, associate with the "Others" region
                        # region_ = Region.objects.get(name="Others")

        #             # Create a new Country instance and save it to the database
        #             country, created = Country.objects.get_or_create(name=country_name, capital=capital, region=region)
        #             if created:
        #                 print(f"Created country: {country.name} (Capital: {country.capital})")

        #             # Associate the country with the region (if a valid region is found)

        #     else:
        #         print("Failed to retrieve data from the API.")
        # except requests.exceptions.RequestException as e:
        #     print("An error occurred:", e)

        countries = Country.objects.all().order_by("name")
        response = self.paginate_queryset(countries, request, view=self)
        serializer = CountrySerializer(response, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)
        return self.get_paginated_response(serializer.data)


class CountryAndPaymentMethods(APIView, PageNumberPagination):
    def get(self, request):
        payment_options = PaymentOption.objects.all().order_by("payment_option")
        response = self.paginate_queryset(payment_options, request, view=self)
        serializer = CountryPaymentOptionSerializer(response, many=True)
        # return Response(serializer.data)
        return self.get_paginated_response(serializer.data)

class AllRegion(APIView):
    def get(self, request):
        regions = Region.objects.all().order_by("name")
        serializer = RegionSerializer(regions, many=True)
        return Response(serializer.data, status.HTTP_200_OK)