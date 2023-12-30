import secrets

from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings


def send_confirmation_email(email) -> None:
    unique_link = _generate_unique_link()

    subject = 'Registration Confirmation'
    message = f'Link to profile {unique_link}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)


def _generate_unique_link() -> str:
    link_key = secrets.token_urlsafe(12)
    redirect_url = reverse('profile', args=[link_key])

    return f'http://127.0.0.1:8000{redirect_url}'

