from rest_framework import serializers
from django.core.exceptions import ValidationError
import re
from .models import *
from countries.models import Country


class WaitListSerializer(serializers.ModelSerializer):
    class Meta:
        model = WaitList
        fields = "__all__"

    def validate_email(self, value):
        if WaitList.objects.filter(email=value).exists():
            raise ValidationError("User with this email already exists")
        return value

class RegisterSerializer(serializers.ModelSerializer):
    industry = serializers.SlugRelatedField(
        slug_field="name", queryset=Industry.objects.all())
    country = serializers.SlugRelatedField(
        slug_field="name", queryset=Country.objects.all())

    class Meta:
        model = AppUser
        fields = ["account_type", "job_status", "employment_type",
                  "job_role", "country", "industry", "first_name",
                  "last_name", "email", "password", "agree",]

        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_password(self, value):
        if len(value) < 8:
            raise ValidationError(
                "Password must be at least 8 characters long")
        if not any(char.isupper() for char in value):
            raise ValidationError(
                "Password must contain at least one uppercase letter")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValidationError(
                "Password must contain at least one special character")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = self.Meta.model(**validated_data)

        if password:
            user.set_password(password)
        user.save()
        return user



class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = ["name"]