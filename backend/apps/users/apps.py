"""Users app."""
from django.apps import AppConfig

class UsersConfig(AppConfig):
    """Users app configuration."""
    name = "backend.apps.users"
    verbose_name = "Users"
    default_auto_field = 'django.db.models.BigAutoField'
    label = "users"