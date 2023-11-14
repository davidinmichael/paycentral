from django.shortcuts import redirect, render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import *
from .models import *
from .utils import *


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


class ResendVerificationMail(APIView):
    def get(self, request, user_email):
        user = AppUser.objects.get(email=user_email)
        if user.email_verified == False:
            context = {
                "name": user.first_name,
                "email": user.email,
                "token": user.token_otp,
            }
            template = render_to_string("account/welcome_email.html", context)
            print(template)
            try:
                send_email(user.email, template)
                return Response({"message": "Email Sent"}, status.HTTP_200_OK)
            except:
                return Response({"message": "Try Again"}, status.HTTP_200_OK)


class VerifyEmail(APIView):
    def get(self, request, token):
        url = "https://github.com/davidinmichael/paycentral"
        user = AppUser.objects.get(token_otp=token)
        if user.email == False:
            user.email_verified = True
            user.save()
            return redirect(url)
        else:
            return redirect("https://github.com/davidinmichael/articleapp")