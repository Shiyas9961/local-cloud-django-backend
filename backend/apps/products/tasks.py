"""Tasks module."""

import os
import time

from backend.apps.core.utils.s3 import upload_and_get_url
from backend.apps.products.models import Product
from backend.apps.products.services import ProductService
from backend.celery import app


@app.task(queue="default")
def cleanup_unuploaded_products():
    """Delete products where image was not uploaded successfully."""
    products = Product.objects.filter(is_image_uploaded=False)
    count = products.count()
    products.delete()

    return f"Deleted {count} unapplied products"


@app.task(queue="default")
def upload_product_image_task(product_id, original_file_name, file_bytes):
    """Upload a file for a product."""
    product = Product.objects.get(id=product_id)

    # Extract extension from original filename (keep dot)
    _, ext = os.path.splitext(original_file_name)
    ext = ext.lower() if ext else ".bin"

    # Build final filename exactly as requested
    timestamp = int(time.time())
    final_file_name = f"product_{product_id}_{timestamp}{ext}"

    image_url = upload_and_get_url(
        file_bytes=file_bytes,
        folder_name="products",
        final_filename=final_file_name,
    )

    product.image_url = image_url
    product.is_image_uploaded = True
    product.save(update_fields=["image_url", "is_image_uploaded"])


@app.task(queue="default")
def update_product_stats_task():
    stats = ProductService.update_stats()
    return stats
