import pytest
from rest_framework.test import APIClient

from users.models import User


@pytest.fixture
def user():
    user = User.objects.create_user(
        phone="+77057421693",
        first_name="testt",
        password="Agds8751A!sacAD",
        birth_date='2004-05-13'
    )

    return user


@pytest.fixture
def client():
    return APIClient()