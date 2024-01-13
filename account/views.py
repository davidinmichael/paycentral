from django.shortcuts import redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.template.loader import render_to_string
from .utils import *
from .serializers import *
from .models import *
from .utils import *



# Create your views here.

class WaitingList(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        waitlist = WaitList.objects.all()
        if waitlist:
            serializer = WaitListSerializer(waitlist, many=True)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            return Response({"message": "No Users in the waitlist yet"}, status.HTTP_200_OK)
        
    def post(self, request):
        data = {}
        serializer = WaitListSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            data["message"] = "We have added you to our waiting list!"
            data["message2"] = "We'll let you know when PayCentral is ready"
            data["email"] = user.email
            return Response(data, status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)

            


class AllIndustries(APIView):

    def get(self, request):
        industry = Industry.objects.all()
        serializer = IndustrySerializer(industry, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


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
                return Response({"message": "Email Sent to your email"}, status.HTTP_200_OK)
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


class ForgotPassword(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        try:
            user = AppUser.objects.get(email=email)
            print(user.id)
        except AppUser.DoesNotExist:
            return Response({"message": "User with that email does not exist"},
                            status.HTTP_404_NOT_FOUND)
        context = {
            "id": user.id,
            "name": user.first_name,
        }
        template = render_to_string("account/forgot_email.html", context)
        try:
            forgot_password_email(user.email, template)
        except:
            return Response({"message": "Error sending mail"}, status.HTTP_400_BAD_REQUEST)
        return Response({"message": f"We have sent an email with a password reset information to {user.email}"}, status.HTTP_200_OK)


class VerifyPasswordLink(APIView):
    permission_classes = [AllowAny]

    def get(self, request, id):
        # url = f"https://github.com/davidinmichael/paycentral/?user_id={id}"
        url = "https://github.com/davidinmichael/paycentral"
        try:
            user = AppUser.objects.get(id=id)
        except AppUser.DoesNotExist:
            return Response({"message": "User does not exist"})
        return redirect(url)
        


class ChangePassword(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_id = request.data.get("user_id")
        password = request.data.get("password")
        confirm_password = request.data.get("confirm_password")

        try:
            user = AppUser.objects.get(id=user_id)
        except AppUser.DoesNotExist:
            return Response({"message": "Invalid URL for password reset"}, status.HTTP_404_NOT_FOUND)
        if password != confirm_password:
            return Response({"message": "Passwords do not match"}, status.HTTP_400_BAD_REQUEST)
        else:
            user.set_password(password)
            user.save()
            return Response({"message": "Password reset successfully!"}, status.HTTP_201_CREATED)
