"""Core application models."""

from django.db import models


class SingletonModel(models.Model):
    """Base singleton model that ensures only one instance exists."""

    class Meta:
        """Meta options"""

        abstract = True

    def save(self, *args, **kwargs):
        """Override save to ensure only one instance exists."""
        self.pk = 1
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Prevent deletion of singleton instance."""
        pass

    @classmethod
    def load(cls):
        """Load the singleton instance, creating it if it doesn't exist."""
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
