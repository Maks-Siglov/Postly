import hashlib

from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse

from users.models import User


def send_confirmation_email(user: User, email: str) -> None:
    link_key = hashlib.md5(email.encode()).hexdigest()
    user.email_hash = link_key
    user.save()
    redirect_url = reverse("profile_registration", args=[link_key])
    unique_link = f"http://127.0.0.1:8000{redirect_url}"

    subject = "Registration Confirmation"
    message = f"Link to profile {unique_link}"
    recipient_list = [email]

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient_list)
