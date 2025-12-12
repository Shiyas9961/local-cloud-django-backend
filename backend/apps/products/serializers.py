"""Products application serializers."""

import logging

from rest_framework import serializers

from backend.apps.products.models import Product
from backend.apps.products.services import ProductService
from backend.apps.products.tasks import upload_product_image_task

LOG = logging.getLogger(__name__)


class ProductSerializer(serializers.ModelSerializer):
    """Products application serializers."""

    image_file = serializers.FileField(write_only=True, required=False)

    class Meta:
        """Meta class for ProductSerializer."""

        model = Product
        fields = (
            "id",
            "name",
            "price",
            "description",
            "stock",
            "image_url",
            "is_image_uploaded",
            "image_file",
        )
        read_only_fields = [
            "id",
            "image_url",
            "is_image_uploaded",
        ]

    def create(self, validated_data):
        """Create a product."""
        if ProductService.is_quota_exceeded():
            raise serializers.ValidationError({"detail": "Product quota exceeded."})

        image_file = validated_data.pop("image_file", None)

        # Step 1: Create product without image_url
        product = Product.objects.create(**validated_data)

        # Read bytes and get original filename
        if image_file:
            original_name = image_file.name or "file"
            file_bytes = image_file.read()

            # Step 2: Trigger the image-upload task.
            # Pass the original filename so the extension is preserved.
            upload_product_image_task.delay(product.id, original_name, file_bytes)

        LOG.info(f"Product {product.id} created successfully.")
        return product
