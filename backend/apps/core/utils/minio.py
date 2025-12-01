import logging

from minio import Minio
from django.conf import settings
import io
import uuid

LOG = logging.getLogger(__name__)

def upload_to_minio_and_get_url(file_name, file_bytes, content_type="image/jpeg"):
    """
    Upload file to MinIO and return public URL.
    """

    # Internal docker connection
    client = Minio(
        settings.MINIO_ENDPOINT,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        secure=False,
    )

    bucket_name = settings.MINIO_BUCKET_NAME

    # Ensure bucket exists
    try:
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)
    except Exception:
        # Bucket may already be being created by another worker — ignore
        LOG.warning(f"Failed to create bucket {bucket_name}: {e}")
        pass

    # Generate unique filename if needed
    if not file_name:
        file_name = f"{uuid.uuid4()}.jpg"

    # Upload object
    client.put_object(
        bucket_name=bucket_name,
        object_name=file_name,
        data=io.BytesIO(file_bytes),
        length=len(file_bytes),
        content_type=content_type,
    )

    # Build public URL (external access)
    # MINIO_PUBLIC_ENDPOINT should be localhost:9000
    public_url = f"http://{settings.MINIO_PUBLIC_ENDPOINT}/{bucket_name}/{file_name}"

    return public_url