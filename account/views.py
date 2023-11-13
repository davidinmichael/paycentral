from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import *

# Create your views here.
class RegisterUsers(APIView):
    def post(self, request):
        data = {}
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        data["message"] = f"We have sent a verification email to {user.email}"
        data["first_name"] = user.first_name
        data["last_name"] = user.last_name
        data["email"] = user.email
        data["country"] = user.country.name
        data["account_type"] = user.account_type
        data["job_status"] = user.job_status
        data["employment_type"] = user.employment_type
        data["job_role"] = user.job_role
        data["industry"] = user.industry.name
        return Response(data, status.HTTP_201_CREATED)
    

