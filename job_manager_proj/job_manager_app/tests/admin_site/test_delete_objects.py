import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.test import Client, TestCase
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
from job_manager_app.tests import fixtures as fixs

pytestmark = [pytest.mark.django_db]


class AdminSiteDeleteObjectTestCase(TestCase):
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
