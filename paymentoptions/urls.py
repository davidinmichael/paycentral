from django.urls import path
from .views import *

urlpatterns = [
    path("all-payment_options/", PaymentOptions.as_view()),
    path("available-payments_countries/", AvailablePaymentOptionAndCountries.as_view()),
    path("payment_option/<str:pk>/", SinglePaymentAndCountries.as_view()),
    path("add_payment_option/", AddPaymentOptions.as_view()),
]