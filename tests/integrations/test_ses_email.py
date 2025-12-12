import boto3
from django.conf import settings


def test_ses_connection():
    client = boto3.client(
        "ses",
        region_name=settings.AWS_REGION_NAME,
        endpoint_url=settings.AWS_ENDPOINT_URL,
    )

    identities = client.list_identities()
    assert "Identities" in identities
