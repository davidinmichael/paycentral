from django.urls import path
from .views import *

urlpatterns = [
    path("payment_methods/", PaymentOptions.as_view()),
    path("add_payment_option/", AddPaymentOptions.as_view()),
    # path("all_countries/", AllCountries.as_view()),
]