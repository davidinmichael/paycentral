from django.urls import path
from .views import *


urlpatterns = [
    path("countries/", Countries.as_view()),
]
