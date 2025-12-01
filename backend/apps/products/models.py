"""Product model."""
from django.db import models
import uuid

class Product(models.Model):
    """Product model."""

    class Meta:
        """Meta options."""
        verbose_name = "Product"
        verbose_name_plural = "Products"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    description = models.TextField(null=True, blank=True)
    stock = models.IntegerField(db_index=True)
    image_url = models.URLField(max_length=2048, null=True, blank=True)
    is_image_uploaded = models.BooleanField(default=False, db_index=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return the name of the product."""
        return self.name