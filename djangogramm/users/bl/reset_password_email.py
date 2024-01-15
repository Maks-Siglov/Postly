import hashlib

from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse

from users.models import User


def send_resetting_password_email(user: User):
    redirect_url = reverse("users:reset_password", args=[user.email_hash])
    unique_link = f"http://127.0.0.1:8000{redirect_url}"

    subject = "Password reset"
    message = f"Here is the link where you can reset your password {unique_link}"
    recipient_list = [user.email]

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
