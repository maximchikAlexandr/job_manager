import pytest
from django.test import TestCase
from django.urls import reverse

from catalog.apps import CatalogConfig
from commerce.apps import CommerceConfig
from management.apps import ManagementConfig
from tests.admin_site import BaseAdminSiteTestCaseMixin

pytestmark = [pytest.mark.django_db]


class AdminSiteGetRequestTestCase(BaseAdminSiteTestCaseMixin, TestCase):
    def test_mainpage_redirect_unauthenticated_user(self):
        url = reverse(f"admin:index")
        response = self.client.get(url)
        self.assertRedirects(
            response, "/login/?next=/", status_code=302, target_status_code=200
        )

    def check_redirect_unauthenticated_user(self, *, name_model, app_name):
        url = reverse(f"admin:{app_name}_{name_model}_changelist")
        response = self.client.get(url)
        self.assertRedirects(
            response,
            f"/login/?next=%2F{app_name}%2F{name_model}%2F",
            status_code=302,
            target_status_code=200,
        )

    def test_employee_redirect_unauthenticated_user(self):
        self.check_redirect_unauthenticated_user(
            name_model="employee", app_name=CatalogConfig.name
        )

    def test_department_redirect_unauthenticated_user(self):
        self.check_redirect_unauthenticated_user(
            name_model="department", app_name=CatalogConfig.name
        )

    def test_headofdepartment_redirect_unauthenticated_user(self):
        self.check_redirect_unauthenticated_user(
            name_model="headofdepartment", app_name=CatalogConfig.name
        )

    def test_company_redirect_unauthenticated_user(self):
        self.check_redirect_unauthenticated_user(
            name_model="company", app_name=CatalogConfig.name
        )

    def test_typeofjob_redirect_unauthenticated_user(self):
        self.check_redirect_unauthenticated_user(
            name_model="typeofjobs", app_name=CatalogConfig.name
        )

    def test_month_redirect_unauthenticated_user(self):
        self.check_redirect_unauthenticated_user(
            name_model="month", app_name=CatalogConfig.name
        )

    def test_budgetcalculation_redirect_unauthenticated_user(self):
        self.check_redirect_unauthenticated_user(
            name_model="budgetcalculation", app_name=CommerceConfig.name
        )

    def test_commercialproposal_redirect_unauthenticated_user(self):
        self.check_redirect_unauthenticated_user(
            name_model="commercialproposal", app_name=CommerceConfig.name
        )

    def test_serviceagreement_redirect_unauthenticated_user(self):
        self.check_redirect_unauthenticated_user(
            name_model="serviceagreement", app_name=CommerceConfig.name
        )
