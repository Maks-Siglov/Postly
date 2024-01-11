from django.test import Client
from django.urls import reverse


def test_main_page(client: Client):
    response = client.get(reverse("main:index"))
    assert response.status_code == 200
