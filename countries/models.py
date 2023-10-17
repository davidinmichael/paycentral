from django.db import models


class Region(models.Model):
    name = models.CharField(max_length=256, unique=True)

    def __str__(self):
        return self.name
    
class Country(models.Model):
    name = models.CharField('Name', max_length=100, unique=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name="countries", null=True)
    capital = models.CharField("Capital", max_length=100)


    def __str__(self):
        return self.name