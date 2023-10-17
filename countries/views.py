from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from bs4 import BeautifulSoup
import lxml
import requests

class Countries(APIView):
    def get(self, request):
        # url = "https://restcountries.com/v3.1/all"

        # try:
        #     response = requests.get(url)

        #     if response.status_code == 200:
        #         data = response.json()

        #         for country_data in data:
        #             country_name = country_data["name"]["common"]
        #             capital = country_data.get("capital", "N/A")

        #             # Create a new Country instance and save it to the database
        #             country, created = Country.objects.get_or_create(name=country_name, capital=capital)
        #             if created:
        #                 print(f"Created country: {country.name} (Capital: {country.capital})")
        #             else:
        #                 print(f"Country already exists: {country.name} (Capital: {country.capital})")

        #     else:
        #         print("Failed to retrieve data from the API.")
        # except requests.exceptions.RequestException as e:
        #     print("An error occurred:", e)
        countries = Country.objects.all()
        serializer = CountrySerializer(countries, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
