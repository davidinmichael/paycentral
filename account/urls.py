from django.urls import path
from .views import *


urlpatterns = [
    path("register/", RegisterUsers.as_view()),
]
