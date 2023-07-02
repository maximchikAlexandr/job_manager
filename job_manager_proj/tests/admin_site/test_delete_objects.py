import pytest
from django.test import TestCase
from django.urls import reverse

from catalog.apps import CatalogConfig
from commerce.apps import CommerceConfig
from management.apps import ManagementConfig

from catalog.models import Company, Month, TypeOfJobs
from commerce.models import ServiceAgreement
from management.models import Employee, MonthJob
from tests.admin_site import BaseAdminSiteTestCaseMixin

pytestmark = [pytest.mark.django_db]


class AdminSiteDeleteObjectTestCase(BaseAdminSiteTestCaseMixin, TestCase):

    def check_delete_object(self, *, model, app_name):
        self.client.login(username=self.TEST_USERNAME, password=self.TEST_PASSWORD)
        obj = model.objects.first()
        model_name = model.__name__.lower()
        url = reverse(
            f"admin:{app_name}_{model_name}_delete", args=(obj.id,)
        )
        response = self.client.post(url, {"post": "yes"})
        self.assertEqual(response.status_code, 302)
        self.assertFalse(model.objects.filter(id=obj.id).exists())

    def test_delete_company(self):
        self.check_delete_object(model=Company, app_name=CatalogConfig.name)

    def test_delete_monthjob(self):
        self.check_delete_object(model=Employee, app_name=ManagementConfig.name)

    def test_delete_monthjob(self):
        self.check_delete_object(model=MonthJob, app_name=ManagementConfig.name)

    def test_delete_month(self):
        self.check_delete_object(model=Month, app_name=CatalogConfig.name)

    def test_delete_serviceagreement(self):
        self.check_delete_object(model=ServiceAgreement, app_name=CommerceConfig.name)

    def test_delete_typeofjob(self):
        self.check_delete_object(model=TypeOfJobs, app_name=CatalogConfig.name)
