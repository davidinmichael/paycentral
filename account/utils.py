from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, EmailMultiAlternatives


def send_email(user_email, template):
    subject = "Verify Your Email!"
    from_email = settings.EMAIL_HOST_USER
    to_email = [user_email]

    email = EmailMultiAlternatives(
        subject=subject,
        body=f"Verify your email:",
        from_email=from_email,
        to=to_email,
    )
    email.content_subtype = "html"
    email.attach_alternative(template, "text/html")

    try:
        email.send(fail_silently=False)
        print("Email sent to, ", user_email)
    except Exception as e:
        print(f"Failed to send email: {e}")
        return f"Couldn't connect, try again"

    return None

def forgot_password_email(user_email, template):
    subject = "Reset Password!"
    from_email = settings.EMAIL_HOST_USER
    to_email = [user_email]

    email = EmailMultiAlternatives(
        subject=subject,
        body=f"Verify your email:",
        from_email=from_email,
        to=to_email,
    )
    email.content_subtype = "html"
    email.attach_alternative(template, "text/html")

    try:
        email.send(fail_silently=False)
        print("Email sent to, ", user_email)
    except Exception as e:
        print(f"Failed to send email: {e}")
        return f"Couldn't connect, try again"

    return None

def waitlist_email(user_email, template):
    subject = "PayCentral Waitlist"
    from_email = settings.EMAIL_HOST_USER
    to_email = [user_email]

    email = EmailMultiAlternatives(
        subject=subject,
        body=f"Verify your email:",
        from_email=from_email,
        to=to_email,
    )
    email.content_subtype = "html"
    email.attach_alternative(template, "text/html")

    try:
        email.send(fail_silently=False)
        print("Email sent to, ", user_email)
    except Exception as e:
        print(f"Failed to send email: {e}")
        return f"Couldn't connect, try again"

    return None
