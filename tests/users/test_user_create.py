import pytest


@pytest.mark.django_db
def test_user_create(api_client):

    url = "/api/users"
    data = {
        "username": "testuser",
        "password": "testpassword",
    }
    res = api_client.post(url, data)

    assert res.status_code == 201
    assert res.data["username"] == "testuser"
