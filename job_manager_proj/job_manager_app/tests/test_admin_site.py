import os

import pytest
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.test import TestCase
from job_manager_app.apps import JobManagerAppConfig
from job_manager_app.tests import PATH_TO_FIXTURES

pytestmark = [pytest.mark.django_db]


class AdminSiteTestCase(TestCase):
    fixtures = [
        f"{PATH_TO_FIXTURES}/{fix}"
        for fix in os.listdir(f"{settings.BASE_DIR}/{PATH_TO_FIXTURES}")
    ]
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

    def test_mainpage(self):
        self.client.login(username=self.TEST_USERNAME, password=self.TEST_PASSWORD)
        response = self.client.get("")
        self.assertEqual(response.status_code, 200)

    def test_actofcompletedwork(self):
        self.client.login(username=self.TEST_USERNAME, password=self.TEST_PASSWORD)
        response = self.client.get(f"/{JobManagerAppConfig.name}/actofcompletedwork/")
        self.assertEqual(response.status_code, 200)

    def test_company(self):
        self.client.login(username=self.TEST_USERNAME, password=self.TEST_PASSWORD)
        response = self.client.get(f"/{JobManagerAppConfig.name}/company/")
        self.assertEqual(response.status_code, 200)

    def test_employee(self):
        self.client.login(username=self.TEST_USERNAME, password=self.TEST_PASSWORD)
        response = self.client.get(f"/{JobManagerAppConfig.name}/employee/")
        self.assertEqual(response.status_code, 200)

    def test_monthjob(self):
        self.client.login(username=self.TEST_USERNAME, password=self.TEST_PASSWORD)
        response = self.client.get(f"/{JobManagerAppConfig.name}/monthjob/")
        self.assertEqual(response.status_code, 200)

    def test_month(self):
        self.client.login(username=self.TEST_USERNAME, password=self.TEST_PASSWORD)
        response = self.client.get(f"/{JobManagerAppConfig.name}/month/")
        self.assertEqual(response.status_code, 200)

    def test_serviceagreement(self):
        self.client.login(username=self.TEST_USERNAME, password=self.TEST_PASSWORD)
        response = self.client.get(f"/{JobManagerAppConfig.name}/serviceagreement/")
        self.assertEqual(response.status_code, 200)

    def test_typeofjob(self):
        self.client.login(username=self.TEST_USERNAME, password=self.TEST_PASSWORD)
        response = self.client.get(f"/{JobManagerAppConfig.name}/typeofjob/")
        self.assertEqual(response.status_code, 200)

    def test_mainpage_redirect_unauthenticated_user(self):
        response = self.client.get("")
        self.assertRedirects(
            response, "/login/?next=/", status_code=302, target_status_code=200
        )

    def check_redirect_unauthenticated_user(self, *, name_model):
        response = self.client.get(f"/{JobManagerAppConfig.name}/{name_model}/")
        self.assertRedirects(
            response, f"/login/?next=%2F{JobManagerAppConfig.name}%2F{name_model}%2F",
            status_code=302, target_status_code=200
        )

    def test_actofcompletedwork_redirect_unauthenticated_user(self):
        self.check_redirect_unauthenticated_user(name_model="actofcompletedwork")

    def test_company_redirect_unauthenticated_user(self):
        self.check_redirect_unauthenticated_user(name_model="company")

    def test_employee_redirect_unauthenticated_user(self):
        self.check_redirect_unauthenticated_user(name_model="employee")

    def test_monthjob_redirect_unauthenticated_user(self):
        self.check_redirect_unauthenticated_user(name_model="monthjob")

    def test_month_redirect_unauthenticated_user(self):
        self.check_redirect_unauthenticated_user(name_model="month")

    def test_serviceagreement_redirect_unauthenticated_user(self):
        self.check_redirect_unauthenticated_user(name_model="serviceagreement")

    def test_typeofjob_redirect_unauthenticated_user(self):
        self.check_redirect_unauthenticated_user(name_model="typeofjob")

