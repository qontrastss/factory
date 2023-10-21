import pytest


@pytest.mark.django_db
def test_register_user(client):
    payload = dict(
        phone="+77057421693",
        first_name="testt",
        password="Agds8751A!sacAD",
        birth_date='2004-05-13'
    )

    response = client.post('/api/v1/user/register/', payload)

    data = response.data

    assert data["phone"] == payload["phone"]
    assert data["first_name"] == payload["first_name"]
    assert data["birth_date"] == payload["birth_date"]
    assert "password" not in data


@pytest.mark.django_db
def test_login_user(client, user):
    response = client.post('/api/v1/user/token/', dict(
        phone="+77057421693",
        password="Agds8751A!sacAD"
    ))

    assert response.status_code == 200


@pytest.mark.django_db
def test_login_user_fail(client, user):
    response = client.post('/api/v1/user/token/', dict(
        phone="+77057421693",
        password="IncorrectPassw243!ord"
    ))
    print(response.status_code)

    assert response.status_code == 401