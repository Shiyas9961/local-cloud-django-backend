from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
import time

def upload_and_get_url(file_bytes, folder_name="media", file_name=None, final_filename=None):
    """
    Saves file_bytes to default_storage and returns the public URL.

    - If final_filename is provided, it's used as-is (no extra timestamping).
      final_filename should include the extension (e.g. "product_1_1610000000.png").
    - If final_filename is not provided, we will generate one using file_name and a timestamp.

    Accepts any file type.
    """
    # Determine extension and base name if final_filename not provided
    if final_filename:
        # sanitize final_filename a little: remove any leading slashes
        final_filename = final_filename.lstrip("/\\")
        filename_to_save = final_filename
    else:
        if not file_name:
            file_name = "file"
        _, ext = os.path.splitext(file_name)
        ext = ext.lower().strip(".") or "bin"
        base = os.path.splitext(file_name)[0]
        timestamp = int(time.time())
        filename_to_save = f"{base}_{timestamp}.{ext}"

    # Ensure folder_name has no leading/trailing slashes
    folder_name = folder_name.strip("/\\")
    file_path = os.path.join(folder_name, filename_to_save)

    # Save using Django storage (S3 / MinIO / local)
    saved_path = default_storage.save(file_path, ContentFile(file_bytes))

    # Return public URL
    return default_storage.url(saved_path)

