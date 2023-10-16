from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from bs4 import BeautifulSoup
import lxml
import requests


url = "https://en.wikipedia.org/wiki/List_of_online_payment_service_providers"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

table = soup.select("tbody tr")
table_data = []
for i in range(6):
    table_data.append([table[i].text.strip()])

results = []

for item in table_data:
    payment_data = item[0].split('\n')

    payment_method = payment_data[0]
    platforms = payment_data[1].split(', ')
    locations = payment_data[2].split(', ')
    
    payment_dict = {
        payment_method: {
            "platform": platforms,
            "location": locations
        }
    }

    results.append(payment_dict)

# Iterate through the scraped data
for item in results:
    payment_method, data = list(item.items())[0]
    platforms = data["platform"]
    locations = data["location"]

    # Create the PaymentOption instance for the payment method
    payment_option_instance, created = PaymentOption.objects.get_or_create(payment_option=payment_method)

    # Create or associate countries with the PaymentOption instance
    for location in locations:
        location = location.strip()
        country_instance, created = Country.objects.get_or_create(name=location)
        
        # Handle duplicates if the name is set to unique
        if not created:
            # If the country already exists, associate it with the PaymentOption instance
            payment_option_instance.country.add(country_instance)
        else:
            # If the country is newly created, add it to the PaymentOption instance
            payment_option_instance.country.add(country_instance)

    # Add platforms to the PaymentOption instance
    payment_option_instance.platforms.set(platforms)

print("Data import completed.")


# class PaymentOptions(APIView):
#     def get(self, request):
