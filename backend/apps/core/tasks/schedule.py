"""Core application tasks schedule."""

from celery.schedules import crontab

from backend.celery import app

app.conf.beat.schedule = {
    "delete-un-uploaded-products-daily": {
        "task": "backend.apps.products.tasks.cleanup_unuploaded_products",
        "schedule": crontab(hour=0, minute=0),
    }
}

app.conf.beat_schedule = {
    "update-product-stats-every-day-midnight": {
        "task": "backend.apps.products.tasks.update_product_stats_task",
        "schedule": crontab(hour=0, minute=0),
    },
}
