from django.db.models.signals import post_save
from .models import *
from django.dispatch import receiver
from django.template.loader import render_to_string
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

@receiver(post_save, sender=WaitList)
def waitlist_welcome_email(sender, instance, created, **kwargs):
    context = {
        "name": instance.full_name,
        "email": instance.email,
    }
    template = render_to_string("account/waitlist_email.html", context)
    if created:
        try:
            waitlist_email(instance.email, template)
        except:
            return "Couldn't connect, try again"
