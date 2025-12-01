from celery.schedules import crontab

from backend.celery import app

app.conf.beat.schedule = {
    "delete-unuploaded-products-daily" : {
        "task": "backend.apps.products.tasks.cleanup_unuploaded_products",
        "schedule": crontab(hour=0, minute=0),
    }
}
