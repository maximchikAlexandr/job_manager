import pytest
from django.test import TestCase
from django.urls import reverse

from job_manager_app.apps import JobManagerAppConfig
from job_manager_app.tests.admin_site import BaseAdminSiteTestCaseMixin

pytestmark = [pytest.mark.django_db]


class AdminSiteGetChangelistTestCase(BaseAdminSiteTestCaseMixin, TestCase):

    def test_mainpage(self):
        self.client.login(username=self.TEST_USERNAME, password=self.TEST_PASSWORD)
        url = reverse(f"admin:index")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_actofcompletedwork(self):
        self.client.login(username=self.TEST_USERNAME, password=self.TEST_PASSWORD)
        url = reverse(f"admin:{JobManagerAppConfig.name}_actofcompletedwork_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Act of completed works")

    def test_company(self):
        self.client.login(username=self.TEST_USERNAME, password=self.TEST_PASSWORD)
        url = reverse(f"admin:{JobManagerAppConfig.name}_company_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Companys")

    def test_employee(self):
        self.client.login(username=self.TEST_USERNAME, password=self.TEST_PASSWORD)
        url = reverse(f"admin:{JobManagerAppConfig.name}_employee_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Employees")

    def test_monthjob(self):
        self.client.login(username=self.TEST_USERNAME, password=self.TEST_PASSWORD)
        url = reverse(f"admin:{JobManagerAppConfig.name}_monthjob_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Month jobs")

    def test_month(self):
        self.client.login(username=self.TEST_USERNAME, password=self.TEST_PASSWORD)
        url = reverse(f"admin:{JobManagerAppConfig.name}_month_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Months")

    def test_serviceagreement(self):
        self.client.login(username=self.TEST_USERNAME, password=self.TEST_PASSWORD)
        url = reverse(f"admin:{JobManagerAppConfig.name}_serviceagreement_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Service agreements")

    def test_typeofjob(self):
        self.client.login(username=self.TEST_USERNAME, password=self.TEST_PASSWORD)
        url = reverse(f"admin:{JobManagerAppConfig.name}_typeofjobs_changelist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Type of jobs")
