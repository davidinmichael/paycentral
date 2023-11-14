from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import smtplib
import ssl
import os

def send_email(user_email, template):
    email = EmailMessage(
        "Verify Your Email!",
        template,
        settings.EMAIL_HOST_USER,
        [user_email],
    )
    email.content_subtype = "text/html"
    email.send(fail_silently=False)
    print("Email sent to, ", user_email)
    return None