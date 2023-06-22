import json
import os

import pytest
from django.test import TestCase

from job_manager_app.tests import fixtures as fixs
from job_manager_app.models import (
    ActOfCompletedWork,
    Company,
    Employee,
    Month,
    MonthJob,
    ServiceAgreement,
    TypeOfJobs,
)

CUSTOM_TYPES = (
    ActOfCompletedWork,
    Company,
    Employee,
    Month,
    MonthJob,
    ServiceAgreement,
    TypeOfJobs,
)

pytestmark = [pytest.mark.django_db]

class ModelsTestCase(TestCase):
    fixtures = fixs

    def setUp(self) -> None:
        """
        Create a dictionary of dictionaries based on json fixtures.
        Fixtures are located in the path 'PATH_TO_FIXTURES'
        """
        for fix_path in self.fixtures:
            with open(fix_path, "r", encoding="utf-8") as fixture_file:
                fixture = json.load(fixture_file)
                attr_name = os.path.basename(fix_path)
                attr_name = attr_name.rstrip(".json")
            setattr(self, attr_name, {})

            for model in fixture:
                getattr(self, attr_name)[model["pk"]] = model["fields"]

    def check_model(self, *, model):
        db_objects = model.objects.all()
        name_model = model.__name__.lower()
        for db_object in db_objects:
            valid_obj: dict = getattr(self, name_model)[db_object.pk]
            for name_field, valid_value_of_field in valid_obj.items():
                db_field = getattr(db_object, str(name_field))
                db_field = (
                    db_field.pk if isinstance(db_field, CUSTOM_TYPES) else db_field
                )
                assert str(db_field) == str(valid_value_of_field), (
                    f"Поле в БД не соответствует исходной фикстуре: "
                    f"'{str(db_field)}' != '{str(valid_value_of_field)}'"
                )

    def test_ActOfCompletedWork(self):
        self.check_model(model=ActOfCompletedWork)

    def test_Company(self):
        self.check_model(model=Company)

    def test_Employee(self):
        self.check_model(model=Employee)

    def test_Month(self):
        self.check_model(model=Month)

    def test_MonthJob(self):
        self.check_model(model=MonthJob)

    def test_ServiceAgreement(self):
        self.check_model(model=ServiceAgreement)

    def test_TypeOfJobs(self):
        self.check_model(model=TypeOfJobs)
