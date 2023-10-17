from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from bs4 import BeautifulSoup
import lxml
import requests


class PaymentOptions(APIView):
    def get(self, request):
        payment_options = PaymentOption.objects.all()
        serializer = PaymentOptionSerializers(payment_options, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AllCountries(APIView):
    def get(self, request):
        countries = CountryWiki.objects.all()
        serializer = CountrySerializer(countries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# class PaymentOptions(APIView):
#     def get(self, request):
#         url = "https://en.wikipedia.org/wiki/List_of_online_payment_service_providers"
#         response = requests.get(url)
#         soup = BeautifulSoup(response.text, 'lxml')

#         table = soup.select("tbody tr")
#         table_data = []
#         if table:
#             for i in range(len(table)):
#                 if i < len(table):
#                     table_data.append([table[i].text.strip()])
#                 else:
#                     print("Table out of bound")
#         else:
#             print("Table empty")

#         results = []

#         for item in table_data:
#             payment_data = item[0].split('\n')

#             if len(payment_data) >= 3:  # Check if there are at least 3 elements
#                 payment_method = payment_data[0]
#                 platforms = payment_data[1].split(', ')
#                 locations = payment_data[2].split(', ')

#                 payment_dict = {
#                     payment_method: {
#                         "platform": platforms,
#                         "location": locations
#                     }
#                 }

#                 results.append(payment_dict)
#             else:
#                 # Handle cases where the payment_data doesn't have enough elements
#                 print("Incomplete data:", payment_data)

# # Rest of your code remains unchanged


#         # Iterate through the scraped data
#         for item in results:
#             payment_method, data = list(item.items())[0]
#             platforms = data["platform"]
#             locations = data["location"]

#             # Create the PaymentOption instance for the payment method
#             payment_option_instance, created = PaymentOption.objects.get_or_create(payment_option=payment_method)

#             # Create or associate countries with the PaymentOption instance
#             for location in locations:
#                 location = location.strip()
#                 country_instance, created = Country.objects.get_or_create(name=location)
                
#                 # Handle duplicates if the name is set to unique
#                 if not created:
#                     # If the country already exists, associate it with the PaymentOption instance
#                     payment_option_instance.country.add(country_instance)
#                 else:
#                     # If the country is newly created, add it to the PaymentOption instance
#                     payment_option_instance.country.add(country_instance)

#             # Add platforms to the PaymentOption instance
#             # payment_option_instance.platforms.set(platforms)

#         print("Data import completed.")
#         return Response({"message": "All done"})
