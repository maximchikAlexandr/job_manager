import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "job_manager_proj.settings")

app = Celery("job_manager")
app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()
