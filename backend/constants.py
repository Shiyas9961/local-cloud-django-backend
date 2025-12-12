"""Constants."""

from django.conf import settings

# Cache configuration
PRODUCT_STATS_CACHE_KEY = f"{settings.PROJECT_PREFIX}:product_stats"
PRODUCT_STATS_CACHE_TIMEOUT = 3600
