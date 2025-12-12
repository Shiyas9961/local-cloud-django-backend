"""Users app utils."""

from django.conf import settings


def default_avatar_url():
    """Return default avatar url."""
    return settings.STATIC_URL + "images/default-avatar.png"
