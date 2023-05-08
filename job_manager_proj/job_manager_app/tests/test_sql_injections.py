import pytest
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.test import TestCase
from django.urls import reverse
from django.db import connection

from job_manager_app.tests import fixtures as fixs

pytestmark = [pytest.mark.django_db]


class TestSQLInjection(TestCase):
    fixtures = fixs
    TEST_USERNAME = "admin"
    TEST_PASSWORD = "12345qwerty"

    def setUp(self):
        password = make_password(self.TEST_PASSWORD)
        self.user = get_user_model().objects.create(
            username=self.TEST_USERNAME,
            email="admin@mail.com",
            password=password,
            is_active=True,
            is_superuser=True,
            is_staff=True,
        )
        self.client.login(
            username=self.TEST_USERNAME,
            password=self.TEST_PASSWORD
        )

    def test_drop_table(self):
        table_name = 'auth_user'
        payload = f"'; DROP TABLE {table_name};--"
        response = self.client.get(f"{reverse('admin:index')}?search={payload}")
        self.assertEqual(response.status_code, 200)
        table_exists = table_name in connection.introspection.table_names()
        self.assertTrue(table_exists, f"Table '{table_name}' doesn't exist")
