import pytest

from tests.factories.product_factory import ProductFactory
from tests.factories.user_factory import UserFactory


@pytest.mark.django_db
def test_product_delete(api_client):
    user = UserFactory()
    api_client.force_authenticate(user=user)
    product = ProductFactory()

    url = f"/api/products/{product.id}"
    res = api_client.delete(url)

    assert res.status_code == 204
