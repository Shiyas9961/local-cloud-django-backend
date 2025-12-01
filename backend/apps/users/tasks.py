import os
import time

from backend.celery import app
from backend.apps.core.utils.s3 import upload_and_get_url
from backend.apps.users.models import User


@app.task(queue="default")
def upload_user_avatar_task(user_id, file_name, file_bytes):
    """
    Upload user avatar to S3/MinIO and update User model.
    File must be stored as: userId_timestamp.ext
    """
    user = User.objects.get(id=user_id)

    # Extract extension safely
    _, ext = os.path.splitext(file_name)
    ext = ext.lower().strip(".") or "bin"  # default extension if missing

    # Generate final filename: userId_timestamp.ext
    timestamp = int(time.time())
    final_filename = f"{user_id}_{timestamp}.{ext}"

    # Upload file to S3/minio/local storage
    image_url = upload_and_get_url(
        file_bytes=file_bytes,
        folder_name="avatars",  # folder for user avatars
        final_filename=final_filename
    )

    # Update DB
    user.avatar_url = image_url
    user.is_avatar_uploaded = True
    user.save(update_fields=["avatar_url", "is_avatar_uploaded"])

    return image_url
