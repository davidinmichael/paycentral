from django.urls import path
from .views import *


urlpatterns = [
    path("countries/", Countries.as_view()),
    path("regions/", AllRegion.as_view()),
    path("countries-payment/", CountryAndPaymentMethods.as_view()),
    # path("country/<str:pk>/", SingleCountry.as_view()),
    path("country/<str:pk>/", SingleCountryAndPayment.as_view()),
]
