from django.db import models

class Country(models.Model):
    name = models.CharField('Name', max_length=100)
    capital = models.CharField("Capital", max_length=100)


    def __str__(self):
        return self.name