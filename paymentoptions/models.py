from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
    

class PaymentOption(models.Model):
    country = models.ManyToManyField(Country, related_name="payment_options")
    payment_option = models.CharField(max_length=255)

    def __str__(self):
        return self.payment_option
