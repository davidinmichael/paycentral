from django.urls import path
from .views import *


urlpatterns = [
    path("register/", RegisterUsers.as_view()),
    path("resend_email/<str:user_email>/", ResendVerificationMail.as_view()),
    path("verify/<str:token>/", VerifyEmail.as_view()),
]
