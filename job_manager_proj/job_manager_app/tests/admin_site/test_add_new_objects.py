import pytest
from django.test import TestCase
from django.urls import reverse

from job_manager_app.apps import JobManagerAppConfig
from job_manager_app.models import (
    ActOfCompletedWork,
    Company,
    Employee,
    Month,
    MonthJob,
    ServiceAgreement,
    TypeOfJob,
)
from job_manager_app.tests.admin_site import BaseAdminSiteTestCaseMixin

pytestmark = [pytest.mark.django_db]


class AdminSiteAddObjectTestCase(BaseAdminSiteTestCaseMixin, TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.client.login(username=self.TEST_USERNAME, password=self.TEST_PASSWORD)

    def test_add_company(self):
        url = reverse(f"admin:{JobManagerAppConfig.name}_company_add")
        data = {"name": 'ОАО "Предприятие тестовое"', "unp": 100011222}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        object_added: bool = Company.objects.filter(name=data["name"]).exists()
        self.assertTrue(object_added)

    def test_add_employee(self):
        url = reverse(f"admin:{JobManagerAppConfig.name}_employee_add")
        data = {
            "name": "Django",
            "surname": "Smith",
            "patronymic": "Djangovich",
            "rate": 1.0,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        object_added: bool = Employee.objects.filter(name=data["name"]).exists()
        self.assertTrue(object_added)

    def test_add_monthjob(self):
        url = reverse(f"admin:{JobManagerAppConfig.name}_monthjob_add")
        data = {"man_hours": 999.0, "employee": 1, "month": 11, "act": 1}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        object_added: bool = MonthJob.objects.filter(
            man_hours=data["man_hours"]
        ).exists()
        self.assertTrue(object_added)

    def test_add_month(self):
        url = reverse(f"admin:{JobManagerAppConfig.name}_month_add")
        data = {
            "start_date": "2024-12-01",
            "end_date": "2024-12-31",
            "count_of_working_days": 20,
            "number_of_employees": 3.5,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        object_added: bool = Month.objects.filter(
            start_date=data["start_date"]
        ).exists()
        self.assertTrue(object_added)

    def test_add_typeofjob(self):
        url = reverse(f"admin:{JobManagerAppConfig.name}_typeofjob_add")
        data = {"name": "test_type"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        object_added: bool = TypeOfJob.objects.filter(name=data["name"]).exists()
        self.assertTrue(object_added)