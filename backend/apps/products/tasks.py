"""Tasks module."""
import time
import os

from backend.celery import app
from backend.apps.products.models import Product
from backend.apps.core.utils.s3 import upload_and_get_url

@app.task(queue="default")
def cleanup_unuploaded_products():
    """
    Delete products where image was not uploaded successfully.
    Run daily at 12 AM.
    """
    products = Product.objects.filter(is_image_uploaded=False)
    count = products.count()
    products.delete()

    return f"Deleted {count} unapplied products"

@app.task(queue="default")
def upload_product_image_task(product_id, original_file_name, file_bytes):
    """
    Upload a file for a product. Resulting filename will be:
      products/product_<product_id>_<timestamp>.<ext>

    original_file_name: the incoming filename (used to get extension if present)
    file_bytes: raw bytes of the file
    """
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