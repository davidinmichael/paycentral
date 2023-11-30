from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.db.models import F
from rest_framework.parsers import FormParser, MultiPartParser
from .models import *
from .serializers import *
from bs4 import BeautifulSoup
import lxml
import requests


class PaymentMethods(APIView, PageNumberPagination):
    parser_classes = [FormParser, MultiPartParser]

    def get(self, request):
        payment_options = PaymentMethod.objects.all()
        response = self.paginate_queryset(payment_options, request, view=self)
        serializer = PaymentMethodSerializer(response, many=True)
        if payment_options:
            return self.get_paginated_response(serializer.data)
        else:
            message = "No payment methods available now, check back soon"
            return Response({'message': message}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        data = {}
        serializer = PaymentMethodSerializer(data=request.data)
        if serializer.is_valid():
            payment_method = serializer.save()
            payment_serializer = PaymentMethodSerializer(payment_method)
            data["message"] = 'Payment method added successfully!'
            data["payment_method"] = payment_serializer.data
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


class PaymentGateways(APIView, PageNumberPagination):
    parser_classes = [FormParser, MultiPartParser]

    def get(self, request):
        payment_gateway = PaymentGateway.objects.all()
        response = self.paginate_queryset(payment_gateway, request, view=self)
        serializer = PaymentGatewaySerializer(response, many=True)
        if payment_gateway:
            return self.get_paginated_response(serializer.data)
        else:
            message = "No payment gateways available now, check back soon"
            return Response({'message': message}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        data = {}
        serializer = PaymentGatewaySerializer(data=request.data)
        if serializer.is_valid():
            payment_gateway = serializer.save()
            payment_serializer = PaymentGatewaySerializer(payment_gateway)
            data["message"] = 'Payment Gateway Created successfully!'
            data["payment_gateway"] = payment_serializer.data
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)



class PaymentGatewayRating(APIView):
    def post(self, request):
        serializer = UserRatingSerializer(data=request.data)
        if serializer.is_valid():
            rating = serializer.save(user=request.user)
            gateway = rating.payment_gateway

            # Fetch the PaymentGateway object
            payment_gateway = PaymentGateway.objects.get(name=gateway)

            # Increment the total ratings and add the new rating
            PaymentGateway.objects.filter(name=gateway).update(
                total_ratings=F('total_ratings') + 1,
                rate_sum=F('rate_sum') + rating.rating
            )

            # Ensure total_ratings is not zero to avoid division by zero
            if payment_gateway.total_ratings > 0:
                # Calculate and update the average rating
                PaymentGateway.objects.filter(name=gateway).update(
                    average_rating=F('rate_sum') / F('total_ratings')
                )

            return Response({"message": "Thank you for rating"}, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)


# class PaymentGatewayRating(APIView):
#     def post(self, request):
#         serializer = UserRatingSerializer(data=request.data)
#         if serializer.is_valid():
#             rating = serializer.save(user=request.user)
#             gateway = rating.payment_gateway

#             rate = int(rating.rating)
#             payment_gateway = PaymentGateway.objects.get(name=gateway)
#             payment_gateway.rate_sum += rate
#             payment_gateway.total_ratings += 1
#             payment_gateway.average_rating = round(
#                 payment_gateway.rate_sum / payment_gateway.total_ratings)
#             payment_gateway.save()
#             return Response({"message": "Thank you for rating"}, status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

# class AvailablePaymentOptionAndCountries(APIView):
#     def get(self, request):
#         payment_options = PaymentOption.objects.all().order_by("payment_option")
#         serializer = PaymentOptionCountrySerializer(payment_options, many=True)
#         return Response(serializer.data, status.HTTP_200_OK)


# class SinglePaymentAndCountries(APIView):
#     def get(self, request, pk):
#         try:
#             payment_option = PaymentOption.objects.get(id=pk)
#         except PaymentOption.DoesNotExist:
#             return Response({"message": "Oops, Requested Payment Option Does Not Exist"})
#         serializer = PaymentOptionCountrySerializer(payment_option)
#         return Response(serializer.data, status.HTTP_200_OK)


# class AddPaymentOptions(APIView):
#     def post(self, request):
#         print(request.data)  # Print the data received in the request
#         serializer = AddPaymentOptionSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         print(serializer.errors)  # Print any serializer errors
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
