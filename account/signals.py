from django.db.models.signals import post_save
from .models import *
from django.dispatch import receiver
from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import smtplib
import ssl
import os
from .utils import *





@receiver(post_save, sender=AppUser)
def send_welcome_email(sender, instance, created, **kwargs):
    context = {
        "name": instance.first_name,
        "email": instance.email,
        "token": instance.token_otp,
    }
    template = render_to_string("account/welcome_email.html", context)
    if created:
        try:
            send_email(instance.email, template)
        except:
            return "Couldn't connect, try again"


# @receiver(post_save, sender=AppUser)
# def send_welcome_email(sender, instance, created, **kwargs):
#     context = {
#         "name": instance.first_name,
#         "email": instance.email,
#         "token": instance.token_otp,
#     }
#     template = render_to_string("account/welcome_email.html", context)
#     print(template)
#     if created:
#         email = EmailMessage(
#             "Verify Your Email!",
#             template,
#             settings.EMAIL_HOST_USER,
#             [instance.email],
#         )
#         # email.fail_silently=False
#         email.content_subtype = "text/html"
#         email.send(fail_silently=False)
#         print("Email sent to, ", instance.email)
#     return None


# @receiver(post_save, sender=AppUser)
# def send_welcome_email(sender, instance, created, **kwargs):
#     context = {
#         "name": instance.first_name,
#         "email": instance.email,
#         "token": instance.token_otp,
#     }
#     template = render_to_string("account/welcome_email.html", context)
#     if created:
#         email = EmailMessage(
#             subject=f"Verify Your Email!",
#             body=template,
#             from_email=settings.EMAIL_HOST_USER,
#         to=[instance.email],
#         )
#         email.content_subtype="text/html"
#         email.send()
#         print("Email sent to, ", instance.email)
#     return None
