"""Products application signals."""

from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from backend.apps.products.models import Product
from backend.apps.products.tasks import update_product_stats_task


@receiver(post_save, sender=Product)
def update_stats_on_save(sender, instance, **kwargs):
    update_product_stats_task.delay()


@receiver(post_delete, sender=Product)
def update_status_on_delete(sender, instance, **kwargs):
    update_product_stats_task.delay()
