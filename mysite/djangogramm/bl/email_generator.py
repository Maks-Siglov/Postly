import secrets
from django.urls import reverse


def generate_unique_link():
    link_key = secrets.token_urlsafe(12)
    redirect_url = reverse('profile', args=[link_key])

    return f'http://127.0.0.1:8000{redirect_url}'

