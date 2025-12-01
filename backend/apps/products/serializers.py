from rest_framework import serializers
from backend.apps.products.models import Product
from backend.apps.products.tasks import upload_product_image_task
import logging

logger = logging.getLogger(__name__)

class ProductSerializer(serializers.ModelSerializer):
    image_file = serializers.FileField(write_only=True, required=True)

    class Meta:
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
        read_only_fields = ["id", "image_url", "is_image_uploaded"]

    def create(self, validated_data):
        image_file = validated_data.pop("image_file")

        # Step 1: Create product without image_url
        product = Product.objects.create(**validated_data)

        # Read bytes and get original filename
        original_name = image_file.name or "file"
        file_bytes = image_file.read()

        # Step 2: Trigger image upload task (pass original filename so extension is preserved)
        upload_product_image_task.delay(product.id, original_name, file_bytes)

        logger.info(f"Product {product.id} created successfully; upload task queued.")
        return product