import pytest

from tests.factories.user_factory import UserFactory


@pytest.mark.django_db
def test_product_create(api_client):
    user = UserFactory()
    api_client.force_authenticate(user=user)

    url = "/api/products"
    data = {
        "name": "Laptop",
        "price": "1299.00",
        "stock": 10,
    }

    res = api_client.post(url, data)

    assert res.status_code == 201
    assert res.data["name"] == "Laptop"
