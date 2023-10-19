from django.urls import path
from .views import *


urlpatterns = [
    path("all-countries/", Countries.as_view()),
    path("all-regions/", AllRegion.as_view()),
    path("all-countries_payments/", CountriesAndPaymentMethods.as_view()),
    path("country/<str:pk>/", SingleCountryAndPayment.as_view()),
]
