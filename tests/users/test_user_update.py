import pytest

from tests.factories.user_factory import UserFactory


@pytest.mark.django_db
def test_user_update(api_client):
    user = UserFactory()

    url = f"/api/users/{user.id}"
    data = {
        "username": "updateduser",
    }
    res = api_client.patch(url, data)

    assert res.status_code == 200
    assert res.data["username"] == "updateduser"
