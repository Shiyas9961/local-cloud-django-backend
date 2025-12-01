"""Users app models."""
import uuid
import os

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom user inheriting from AbstractUser.
    We keep username/email behavior default but add avatar_url.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    avatar_url = models.URLField(max_length=2048, null=True, blank=True)
    is_avatar_uploaded = models.BooleanField(default=False)

    def __str__(self):
        """
        Return a string representation of the user.
        """
        return self.username or self.email or str(self.id)