import pytest


@pytest.mark.django_db
def test_register_user(client):
    payload = dict(
        first_name="Messi",
        username="leomessi",
        password="Agds8751A!sacAD"
    )

    response = client.post('/api/v1/user/register/', payload)

    data = response.data

    assert data["first_name"] == payload["first_name"]
    assert data["username"] == payload["username"]
    assert "password" not in data


@pytest.mark.django_db
def test_login_user(client, user):
    response = client.post('/api/v1/user/auth/', dict(
        username="leomessi",
        password="Agds8751A!sacAD"
    ))

    assert response.status_code == 200


@pytest.mark.django_db
def test_login_user_fail(client, user):
    response = client.post('/api/v1/user/auth/', dict(
        username="randomname",
        password="IncorrectPassw243!ord"
    ))

    assert response.status_code == 403