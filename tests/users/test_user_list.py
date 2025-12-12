import pytest

from tests.factories.user_factory import UserFactory


@pytest.mark.django_db
def test_user_list(api_client):
    UserFactory.create_batch(5)

    url = "/api/users"
    res = api_client.get(url)

    assert res.status_code == 200
    assert len(res.data["results"]) >= 5
