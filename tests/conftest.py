import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient


@pytest.fixture
def user():
    user = User.objects.create_user(
        username="leomessi",
        password="Agds8751A!sacAD",
        first_name="Messi"
    )

    return user


@pytest.fixture
def client():
    return APIClient()