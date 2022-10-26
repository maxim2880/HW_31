import os

import pytest as pytest
from factory import django
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient
from pytest_factoryboy import register

from factories import SelectionFactory, UserFactory, AdFactory
from users.models import User


register(SelectionFactory)
register(UserFactory)
register(AdFactory)


@pytest.fixture
def api_client(db, user, ad):
    client = APIClient()
    token = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.access_token}')
    return client
