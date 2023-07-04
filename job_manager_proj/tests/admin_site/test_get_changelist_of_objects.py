import pytest
from django.test import TestCase
from django.urls import reverse

from catalog.apps import CatalogConfig
from commerce.apps import CommerceConfig
from management.apps import ManagementConfig
from tests.admin_site import BaseAdminSiteTestCaseMixin

pytestmark = [pytest.mark.django_db]


class AdminSiteGetChangelistTestCase(BaseAdminSiteTestCaseMixin, TestCase):

    def test_mainpage(self):
        self.client.login(username=self.TEST_USERNAME, password=self.TEST_PASSWORD)
        url = reverse(f"admin:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_employee(self):
        self.client.login(username=self.TEST_USERNAME, password=self.TEST_PASSWORD)
        url = reverse(f"admin:{CatalogConfig.name}_employee_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Employees")

    def test_department(self):
        self.client.login(username=self.TEST_USERNAME, password=self.TEST_PASSWORD)
        url = reverse(f"admin:{CatalogConfig.name}_department_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Departments")

    def test_headofdepartment(self):
        self.client.login(username=self.TEST_USERNAME, password=self.TEST_PASSWORD)
        url = reverse(f"admin:{CatalogConfig.name}_headofdepartment_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Heads of departments")

    def test_company(self):
        self.client.login(username=self.TEST_USERNAME, password=self.TEST_PASSWORD)
        url = reverse(f"admin:{CatalogConfig.name}_company_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Companies")

    def test_month(self):
        self.client.login(username=self.TEST_USERNAME, password=self.TEST_PASSWORD)
        url = reverse(f"admin:{CatalogConfig.name}_month_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Months")

    def test_typeofjob(self):
        self.client.login(username=self.TEST_USERNAME, password=self.TEST_PASSWORD)
        url = reverse(f"admin:{CatalogConfig.name}_typeofjobs_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Types of jobs")

    def test_serviceagreement(self):
        self.client.login(username=self.TEST_USERNAME, password=self.TEST_PASSWORD)
        url = reverse(f"admin:{CommerceConfig.name}_serviceagreement_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Service agreements")

    def test_budgetcalculation(self):
        self.client.login(username=self.TEST_USERNAME, password=self.TEST_PASSWORD)
        url = reverse(f"admin:{CommerceConfig.name}_budgetcalculation_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Budget calculations")

    def test_commercialproposal(self):
        self.client.login(username=self.TEST_USERNAME, password=self.TEST_PASSWORD)
        url = reverse(f"admin:{CommerceConfig.name}_commercialproposal_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Commercial proposals")
