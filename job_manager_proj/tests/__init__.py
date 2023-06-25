import os

from django.conf import settings

_PATH_TO_FIXTURES = "job_manager_app/tests/fixtures/"

fixtures = [
    f"{_PATH_TO_FIXTURES}/{fix}"
    for fix in os.listdir(f"{settings.BASE_DIR}/{_PATH_TO_FIXTURES}")
]
