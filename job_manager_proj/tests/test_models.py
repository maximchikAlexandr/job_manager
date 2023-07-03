import json
import os

import pytest
from catalog.models import (
    BankBranchAddress,
    Company,
    Month,
    RegisteredAddress,
    TypeOfJobs,
)
from commerce.models import (
    BudgetCalculation,
    CommercialProposal,
    PlannedBusinessTrip,
    ServiceAgreement,
)
from django.test import TestCase
from management.models import Department, Employee, HeadOfDepartment, MonthJob
from tests import fixtures as fixs

CUSTOM_TYPES = (
    BankBranchAddress,
    Company,
    Month,
    RegisteredAddress,
    TypeOfJobs,
    BudgetCalculation,
    CommercialProposal,
    PlannedBusinessTrip,
    ServiceAgreement,
    Department,
    Employee,
    HeadOfDepartment,
    MonthJob
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
                attr_name = attr_name.replace(".json", "")
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

    def test_company(self):
        self.check_model(model=Company)

    def test_bank_branch_address(self):
        self.check_model(model=BankBranchAddress)

    def test_registered_address(self):
        self.check_model(model=RegisteredAddress)

    def test_type_of_jobs(self):
        self.check_model(model=TypeOfJobs)

    def test_month(self):
        self.check_model(model=Month)

    def test_planned_business_trip(self):
        self.check_model(model=PlannedBusinessTrip)

    def test_budgetcalculation(self):
        self.check_model(model=BudgetCalculation)

    def test_commercialproposal(self):
        self.check_model(model=CommercialProposal)

    def test_service_agreement(self):
        self.check_model(model=ServiceAgreement)

    def test_employee(self):
        self.check_model(model=Employee)

    def test_month_job(self):
        self.check_model(model=MonthJob)

    def test_department(self):
        self.check_model(model=Department)

    def test_headofdepartment(self):
        self.check_model(model=HeadOfDepartment)
