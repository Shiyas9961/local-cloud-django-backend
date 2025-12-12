import logging

import boto3
from django.conf import settings


def test_cloudwatch_logs():
    logger = logging.getLogger("backend.test")
    logger.error("CloudWatch test error")

    client = boto3.client(
        "logs",
        region_name=settings.AWS_REGION_NAME,
        endpoint_url=settings.AWS_ENDPOINT_URL,
    )

    groups = client.describe_log_groups()
    assert any(
        settings.AWS_CLOUDWATCH_LOG_GROUP in g["logGroupName"]
        for g in groups["logGroups"]
    )
