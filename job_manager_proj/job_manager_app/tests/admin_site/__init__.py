from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password

from job_manager_app.tests import fixtures as fixs


class BaseAdminSiteTestCaseMixin:
    fixtures = fixs
    TEST_USERNAME = "admin"
    TEST_PASSWORD = "12345qwerty"

    def setUp(self) -> None:
        password = make_password(self.TEST_PASSWORD)
        self.user = get_user_model().objects.create(
            username=self.TEST_USERNAME,
            email="admin@mail.com",
            password=password,
            is_active=True,
            is_superuser=True,
            is_staff=True,
        )