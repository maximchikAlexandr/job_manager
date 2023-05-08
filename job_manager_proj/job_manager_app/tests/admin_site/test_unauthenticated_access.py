import pytest
from django.test import TestCase
from django.urls import reverse

from job_manager_app.apps import JobManagerAppConfig
from job_manager_app.tests.admin_site import BaseAdminSiteTestCaseMixin

pytestmark = [pytest.mark.django_db]


class AdminSiteGetRequestTestCase(BaseAdminSiteTestCaseMixin, TestCase):
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
