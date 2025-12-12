import pytest

from tests.factories.product_factory import ProductFactory
from tests.factories.user_factory import UserFactory


@pytest.mark.django_db
def test_product_list(api_client):
    user = UserFactory()
    api_client.force_authenticate(user=user)
    ProductFactory.create_batch(5)

    url = "/api/products"
    res = api_client.get(url)

    assert res.status_code == 200
    assert len(res.data["results"]) >= 5
