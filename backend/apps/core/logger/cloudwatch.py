import watchtower
import boto3
from django.conf import settings

class LocalStackHandler(watchtower.CloudWatchLogHandler):
    def __init__(self, *args, **kwargs):
        session = boto3.session.Session(
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
            region_name=settings.AWS_S3_REGION_NAME,
        )

        super().__init__(
            log_group=settings.AWS_CLOUDWATCH_LOG_GROUP,
            stream_name=settings.AWS_CLOUDWATCH_STREAM_NAME,
            use_queues=False,
            create_log_group=True,
            # no boto3_session here!!
            boto3_client=session.client(
                "logs",
                endpoint_url=settings.AWS_S3_ENDPOINT_URL,  # LocalStack
            ),
        )