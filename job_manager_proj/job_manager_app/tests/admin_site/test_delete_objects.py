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


class AdminSiteDeleteObjectTestCase(BaseAdminSiteTestCaseMixin, TestCase):

    def check_delete_object(self, *, model):
        self.client.login(username=self.TEST_USERNAME, password=self.TEST_PASSWORD)
        obj = model.objects.first()
        model_name = model.__name__.lower()
        url = reverse(
            f"admin:{JobManagerAppConfig.name}_{model_name}_delete", args=(obj.id,)
        )
        response = self.client.post(url, {"post": "yes"})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(model.objects.filter(id=obj.id).exists())

    def test_delete_actofcompletedwork(self):
        self.check_delete_object(model=ActOfCompletedWork)

    def test_delete_company(self):
        self.check_delete_object(model=Company)

    def test_delete_monthjob(self):
        self.check_delete_object(model=Employee)

    def test_delete_monthjob(self):
        self.check_delete_object(model=MonthJob)

    def test_delete_month(self):
        self.check_delete_object(model=Month)

    def test_delete_serviceagreement(self):
        self.check_delete_object(model=ServiceAgreement)

    def test_delete_typeofjob(self):
        self.check_delete_object(model=TypeOfJob)
