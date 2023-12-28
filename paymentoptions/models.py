from email.policy import default
from django.db import models
from countries.models import *
from account.models import AppUser


class PaymentMethod(models.Model):
    name = models.CharField(max_length=50, unique=True)
    logo = models.ImageField(upload_to="payment_option/",
                             default="payment-option.png/")

    def __str__(self):
        return self.name


class PaymentGateway(models.Model):
    name = models.CharField(max_length=50, unique=True)
    payment_options = models.ManyToManyField(PaymentMethod)
    countries = models.ManyToManyField(Country)
    bio = models.TextField()
    about = models.TextField()
    accepted_methods = models.TextField(null=True, blank=True)
    target_audience = models.TextField(null=True, blank=True)
    logo = models.ImageField(upload_to="payment_gateway/",
                             default="payment-gateway.png/")
    rate_sum = models.IntegerField(default=0, blank=True)
    total_ratings = models.IntegerField(default=0, blank=True)
    average_rating = models.IntegerField(default=0, blank=True)

    def __str__(self):
        return f"{self.name} | {self.total_ratings}"


class UserRating(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE, blank=True)
    payment_gateway = models.ForeignKey(
        PaymentGateway, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{str(self.payment_gateway)} | {self.rating}"
