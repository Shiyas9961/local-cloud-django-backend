"""Product service for managing product state and operations."""

import logging
from typing import Dict

from django.core.cache import cache

from backend.apps.products.models import Product, ProductSettings
from backend.constants import PRODUCT_STATS_CACHE_KEY, PRODUCT_STATS_CACHE_TIMEOUT

LOG = logging.getLogger(__name__)


class ProductService:
    """Service class for product operations and state management."""

    @staticmethod
    def get_settings() -> ProductSettings:
        """
        Get product settings singleton instance.

        Returns:
            ProductSettings: The singleton settings instance
        """
        return ProductSettings.load()

    @staticmethod
    def get_stats(use_cache: bool = True) -> Dict:
        """
        Get product statistics.

        Args:
            use_cache: Whether to use cached stats (default: True)

        Returns:
            Dict containing product statistics
        """
        if use_cache:
            stats = cache.get(PRODUCT_STATS_CACHE_KEY)
            if stats is not None:
                return stats

        settings = ProductSettings.load()
        total = Product.objects.count()

        stats = {
            "total": total,
            "quota": settings.quota,
            "remaining": max(0, settings.quota - total),
            "is_quota_exceeded": total >= settings.quota,
            "quota_usage_percentage": (
                (total / settings.quota * 100) if settings.quota > 0 else 0
            ),
        }

        cache.set(PRODUCT_STATS_CACHE_KEY, stats, PRODUCT_STATS_CACHE_TIMEOUT)
        return stats

    @staticmethod
    def invalidate_cache():
        """Invalidate product stats cache."""
        cache.delete(PRODUCT_STATS_CACHE_KEY)
        LOG.debug("Product stats cache invalidated")

    @staticmethod
    def update_stats() -> Dict:
        """
        Force update product statistics in cache.

        Returns:
            Dict containing updated statistics
        """
        try:
            # Invalidate cache and get fresh stats
            ProductService.invalidate_cache()
            stats = ProductService.get_stats(use_cache=False)

            LOG.info(f"Product stats updated: {stats}")
            return stats

        except Exception as e:
            LOG.error(f"Error updating product stats: {str(e)}")
            raise

    @staticmethod
    def is_quota_exceeded() -> bool:
        """
        Check if product quota is exceeded.

        Returns:
            bool: True if quota is exceeded, False otherwise
        """
        stats = ProductService.get_stats()
        return stats["is_quota_exceeded"]

    @staticmethod
    def has_quota_available() -> bool:
        """
        Check if quota is available for new products.

        Returns:
            bool: True if quota is available, False otherwise
        """
        return not ProductService.is_quota_exceeded()

    @staticmethod
    def get_remaining_quota() -> int:
        """
        Get remaining product quota.

        Returns:
            int: Number of products that can still be created
        """
        stats = ProductService.get_stats()
        return stats["remaining"]

    @staticmethod
    def get_quota_info() -> Dict:
        """
        Get detailed quota information.

        Returns:
            Dict containing quota details
        """
        stats = ProductService.get_stats()
        settings = ProductSettings.load()

        return {
            "quota": settings.quota,
            "used": stats["total"],
            "remaining": stats["remaining"],
            "is_exceeded": stats["is_quota_exceeded"],
            "usage_percentage": stats["quota_usage_percentage"],
            "can_create": not stats["is_quota_exceeded"],
        }
