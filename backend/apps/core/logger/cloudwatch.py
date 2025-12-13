"""Cloudwatch logger."""

import logging

import boto3
import watchtower
from django.conf import settings


class LocalStackHandler(watchtower.CloudWatchLogHandler):
    """LocalStack handler for CloudWatch."""

    def __init__(self, *args, **kwargs):
        """Initialize the handler."""
        try:

            session = boto3.session.Session(
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION_NAME,
            )

            super().__init__(
                log_group_name=settings.AWS_CLOUDWATCH_LOG_GROUP,
                log_stream_name=settings.AWS_CLOUDWATCH_STREAM_NAME,
                use_queues=False,
                create_log_group=True,
                # no boto3_session here!!
                boto3_client=session.client(
                    "logs",
                    endpoint_url=settings.AWS_ENDPOINT_URL,  # LocalStack
                ),
            )
        except Exception as e:
            logging.getLogger(__name__).error(
                f"Failed to initialize CloudWatch handler: {e}"
            )
