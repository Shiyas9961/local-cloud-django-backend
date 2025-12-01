"""Application configuration for the auth app."""
from django.apps import AppConfig

class AuthConfig(AppConfig):
    """Auth app configuration."""
    default_auto_field = "django.db.models.BigAutoField"
    verbose_name = "Auth"
    name = "backend.apps.auth"
    label = "custom_auth"
