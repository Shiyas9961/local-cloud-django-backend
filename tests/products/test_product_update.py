import pytest

from tests.factories.product_factory import ProductFactory
from tests.factories.user_factory import UserFactory


@pytest.mark.django_db
def test_product_update(api_client):
    user = UserFactory()
    api_client.force_authenticate(user=user)
    product = ProductFactory()

    url = f"/api/products/{product.id}"
    data = {
        "name": "Updated Product",
        "price": "199.99",
    }
    res = api_client.patch(url, data)

    assert res.status_code == 200
    assert res.data["name"] == "Updated Product"
