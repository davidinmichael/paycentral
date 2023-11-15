from django.urls import path
from .views import *

from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    path("register/", RegisterUsers.as_view()),
    path("resend_email/<str:user_email>/", ResendVerificationMail.as_view()),
    path("verify/<str:token>/", VerifyEmail.as_view()),
    path("login/", LoginUser.as_view()),
]
