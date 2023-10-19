from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from .models import *
from .serializers import *
from bs4 import BeautifulSoup
import lxml
import requests


class PaymentOptions(APIView, PageNumberPagination):
    def get(self, request):
        payment_options = PaymentOption.objects.all()
        response = self.paginate_queryset(payment_options, request, view=self)
        serializer = PaymentOptionSerializers(response, many=True)
        if payment_options:
            return self.get_paginated_response(serializer.data)
        else:
            message = "No payment options available now, check back soon"
            return Response({'message': message}, status=status.HTTP_404_NOT_FOUND)


class AddPaymentOptions(APIView):
    def post(self, request):
        print(request.data)  # Print the data received in the request
        serializer = AddPaymentOptionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)  # Print any serializer errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Getting payment data
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
