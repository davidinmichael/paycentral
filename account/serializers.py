from rest_framework import serializers
from django.core.exceptions import ValidationError
import re
from .models import *


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ["account_type", "job_status", "employment_type",
                  "job_role", "country", "industry", "first_name",
                  "last_name", "email", "password", "agree",]
        
        extra_kwargs = {
            'password': {'write_only': True},
        }
    
    def validate_password(value):
        if len(value) < 8:
            raise ValidationError("Password must be at least 8 characters long")
        if not any(char.isupper() for char in value):
            raise ValidationError("Password must contain at least one uppercase letter")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise ValidationError("Password must contain at least one special character")
