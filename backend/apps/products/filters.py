"""Products application filters."""

import django_filters

from backend.apps.products.models import Product


class ProductFilter(django_filters.FilterSet):
    """Products application filters."""

    min_price = django_filters.NumberFilter(
        field_name="price",
        lookup_expr="gte",
    )
    max_price = django_filters.NumberFilter(
        field_name="price",
        lookup_expr="lte",
    )

    class Meta:
        """Meta class."""

        model = Product
        fields = [
            "min_price",
            "max_price",
        ]
