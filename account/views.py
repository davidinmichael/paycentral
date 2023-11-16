from django.shortcuts import redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from .models import *
from .utils import *


# Create your views here.
class RegisterUsers(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = {}
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
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
        data["token"] = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        return Response(data, status.HTTP_201_CREATED)


class ResendVerificationMail(APIView):
    permission_classes = [AllowAny]

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
    permission_classes = [AllowAny]

    def get(self, request, token):
        url = "https://github.com/davidinmichael/paycentral"
        user = AppUser.objects.get(token_otp=token)
        if user.email_verified == False:
            user.email_verified = True
            user.save()
            return redirect(url)
        else:
            return redirect("https://github.com/davidinmichael/articleapp")


class LoginUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        data = {}

        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = AppUser.objects.get(email=email)
        except AppUser.DoesNotExist:
            return Response({"message": "User with that email does not exist"}, status.HTTP_404_NOT_FOUND)

        if user.check_password(password):
            refresh = RefreshToken.for_user(user)
            data["message"] = f"Welcome back {user.first_name}, you have been logged in"
            data["first_name"] = user.first_name
            data["last_name"] = user.last_name
            data["email"] = user.email
            data["country"] = user.country.name
            data["account_type"] = user.account_type
            data["job_status"] = user.job_status
            data["employment_type"] = user.employment_type
            data["job_role"] = user.job_role
            data["industry"] = user.industry.name
            data["token"] = {
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            }
            return Response(data, status.HTTP_200_OK)
        else:
            return Response({"message": "Incorrect password entered"})



class LogoutUser(APIView):

    def post(self, request):
        refresh_token = request.data.get('refresh_token')

        if not refresh_token:
            return Response({'error': 'Refresh token is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Logout successful, login to continue.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': f'Error logging out: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)