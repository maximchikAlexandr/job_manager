import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.test import TestCase
from django.urls import reverse
from job_manager_app.apps import JobManagerAppConfig
from job_manager_app.tests import fixtures as fixs

pytestmark = [pytest.mark.django_db]


class AdminSiteGetRequestTestCase(TestCase):
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

    def test_mainpage_redirect_unauthenticated_user(self):
        url = reverse(f"admin:index")
        response = self.client.get(url)
        self.assertRedirects(
            response, "/login/?next=/", status_code=302, target_status_code=200
        )

    def check_redirect_unauthenticated_user(self, *, name_model):
        url = reverse(f"admin:{JobManagerAppConfig.name}_{name_model}_changelist")
        response = self.client.get(url)
        self.assertRedirects(
            response,
            f"/login/?next=%2F{JobManagerAppConfig.name}%2F{name_model}%2F",
            status_code=302,
            target_status_code=200,
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
