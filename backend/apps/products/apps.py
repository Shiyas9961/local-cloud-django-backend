"""Application configuration for the products app."""
from django.apps import AppConfig

class ProductsConfig(AppConfig):
    """Products app configuration."""
    default_auto_field = 'django.db.models.BigAutoField'
    verbose_name = "Products"
    name = 'backend.apps.products'
    label = "products"