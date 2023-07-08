import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "job_manager_proj.settings")

app = Celery("job_manager")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()

app.conf.beat_schedule = {
    "every": {
        "task": "commerce.tasks.check_deal_stage_task",
        "schedule": crontab(minute="*/30"),
    },
}