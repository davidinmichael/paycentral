from django.urls import path
from .views import *

from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path("industries/", AllIndustries.as_view()),

    path("register/", RegisterUsers.as_view()),
    path("resend_email/<str:user_email>/", ResendVerificationMail.as_view()),
    path("verify/<str:token>/", VerifyEmail.as_view()),
    path("login/", LoginUser.as_view()),
    path("logout/", LogoutUser.as_view()),

    path("reset_password/", ForgotPassword.as_view()),
    path("reset_password/<str:id>/", VerifyPasswordLink.as_view()),
    path("change_password/", ChangePassword.as_view()),
]
