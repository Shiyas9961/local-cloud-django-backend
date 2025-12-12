"""Users app serializers."""

import logging
import os
import time

from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.db import transaction
from rest_framework import serializers

from backend.apps.core.constants import EMAIL_TEMPLATES
from backend.apps.core.tasks.send_email import send_html_email
from backend.apps.core.utils.s3 import upload_and_get_url
from backend.apps.users.models import User
from backend.apps.users.tasks import upload_user_avatar_task

LOG = logging.getLogger(__name__)


class UserSerializer(serializers.ModelSerializer):
    """User serializer."""

    avatar_file = serializers.FileField(
        required=False, write_only=True, allow_null=True
    )

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "is_staff",
            "is_active",
            "is_avatar_uploaded",
            "avatar_url",
            "avatar_file",
        ]
        read_only_fields = [
            "id",
            "is_avatar_uploaded",
            "avatar_url",
        ]
        extra_kwargs = {
            "password": {
                "write_only": True,
                "required": True,
            }
        }

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError({"password": e.messages})
        return value

    def update(self, instance, validated_data):
        avatar_file = validated_data.pop("avatar_file", None)
        user_id = instance.id

        if avatar_file:
            try:
                # Extract extension safely
                file_name = avatar_file.name
                _, ext = os.path.splitext(file_name)
                ext = ext.lower().strip(".") or "bin"  # default extension if missing

                # Generate final filename: userId_timestamp.ext
                timestamp = int(time.time())
                final_filename = f"{user_id}_{timestamp}.{ext}"

                avatar_url = upload_and_get_url(
                    file_bytes=avatar_file.read(),
                    folder_name="avatars",
                    file_name=final_filename,
                )
                instance.avatar_url = avatar_url
                instance.is_avatar_uploaded = True
            except Exception as e:
                LOG.error(f"Failed to upload avatar: {e}")
                instance.is_avatar_uploaded = False

        return super().update(instance, validated_data)

    def create(self, validated_data):
        avatar_file = validated_data.pop("avatar_file", None)
        password = validated_data.pop("password")

        with transaction.atomic():
            user = User(**validated_data)
            user.set_password(password)
            user.is_active = True
            user.save()

            if avatar_file:
                upload_user_avatar_task.delay(
                    user.id, avatar_file.name, avatar_file.read()
                )

        transaction.on_commit(
            lambda: send_html_email.delay(
                template_name=EMAIL_TEMPLATES.get("USER_WELCOME"),
                subject="User Registration",
                to_email=user.email,
                context={"id": user.id, "email": user.email, "username": user.username},
            )
        )

        return user
