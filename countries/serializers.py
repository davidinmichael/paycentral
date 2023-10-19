from rest_framework import serializers
from .models import *

class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ["name"]

class CountrySerializer(serializers.ModelSerializer):
    region = serializers.StringRelatedField()
    class Meta:
        model = Country
        fields = ["name", "capital", "region"]


