from django.db import models
from countries.models import *
from account.models import AppUser


class PaymentOption(models.Model):
    name = models.CharField(max_length=50, unique=True)
    logo = models.ImageField(upload_to="payment_option/")

    def __str__(self):
        return self.name


class PaymentGateway(models.Model):
    name = models.CharField(max_length=50, unique=True)
    payment_options = models.ManyToManyField(PaymentOption)
    countries = models.ManyToManyField(Country)
    bio = models.TextField()
    about = models.TextField()
    target_audience = models.TextField()
    logo = models.ImageField(upload_to="payment_gateway/")
    total_ratings = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.name} | {self.total_ratings}"


class UserRating(models.Model):
    user = models.ForeignKey(AppUser, on_delete=models.CASCADE)
    payment_gateway = models.ForeignKey(
        PaymentGateway, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{str(self.payment_gateway)} | {self.rating}"
