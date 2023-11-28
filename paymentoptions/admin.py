from django.contrib import admin
from .models import *

admin.site.register(PaymentMethod)
admin.site.register(PaymentGateway)
admin.site.register(UserRating)

# Register your models here.
