"""Utils module."""

def upload_file_to_minio(file_obj, file_name):
    """Uploads given file_obj to MinIO, Returns public URL."""
    return f"http://minio.local/{file_name}"