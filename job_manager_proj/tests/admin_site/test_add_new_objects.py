import pytest
from django.test import TestCase
from django.urls import reverse

from catalog.apps import CatalogConfig
from catalog.models import (
    BankBranchAddress,
    Company,
    Department,
    Employee,
    HeadOfDepartment,
    Month,
    RegisteredAddress,
    TypeOfJobs,
)
from commerce.apps import CommerceConfig
from commerce.models import (
    BudgetCalculation,
    CommercialProposal,
    PlannedBusinessTrip,
    ServiceAgreement,
)
from management.apps import ManagementConfig
from management.models import MonthJob
from tests.admin_site import BaseAdminSiteTestCaseMixin

pytestmark = [pytest.mark.django_db]


class AdminSiteAddObjectTestCase(BaseAdminSiteTestCaseMixin, TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.client.login(username=self.TEST_USERNAME, password=self.TEST_PASSWORD)

    def test_add_employee(self):
        url = reverse(f"admin:{CatalogConfig.name}_employee_add")
        data = {
            "name": "Django",
            "surname": "Smith",
            "patronymic": "Djangovich",
            "rate": 1.0,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        object_added: bool = Employee.objects.filter(
            name=data["name"],
            surname=data["surname"],
            patronymic=data["patronymic"],
            rate=data["rate"]
        ).exists()
        self.assertTrue(object_added)

    def test_add_department(self):
        url = reverse(f"admin:{CatalogConfig.name}_department_add")
        data = {
            "name": "Тестовый отдел",
            "head": 3
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        object_added: bool = Department.objects.filter(
            name=data["name"]
        ).exists()
        self.assertTrue(object_added)

    def test_add_headofdepartment(self):
        url = reverse(f"admin:{CatalogConfig.name}_headofdepartment_add")
        data = {
            "employee": 73
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        object_added: bool = HeadOfDepartment.objects.filter(
            employee=data["employee"]
        ).exists()
        self.assertTrue(object_added)

    def test_add_month(self):
        url = reverse(f"admin:{CatalogConfig.name}_month_add")
        data = {
            "start_date": "2024-12-01",
            "end_date": "2024-12-31",
            "count_of_working_days": 20,
            "number_of_employees": 3.5,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        object_added: bool = Month.objects.filter(
            start_date=data["start_date"],
            end_date=data["end_date"],
            count_of_working_days=data["count_of_working_days"],
            number_of_employees=data["number_of_employees"]
        ).exists()
        self.assertTrue(object_added)

    def test_add_company(self):
        url = reverse(f"admin:{CatalogConfig.name}_company_add")
        data = {
            "name": "ОАО \"Тестовое предприятие\"",
            "unp": "20241231",
            "IBAN": "BY20OLMP3135499711421",
            "bank_name": "ОАО \"Белорусский тестовый банк\"",
            "BIC": "AKBBBY11651",

            "registeredaddress-TOTAL_FORMS": 1,
            "registeredaddress-INITIAL_FORMS": 0,
            "registeredaddress-MIN_NUM_FORMS": 0,
            "registeredaddress-MAX_NUM_FORMS": 1,
            "registeredaddress-0-postal_code": 220099,
            "registeredaddress-0-region": "Гродненская обл.",
            "registeredaddress-0-district": "Гродненский р-н",
            "registeredaddress-0-locality": "Гродно",
            "registeredaddress-0-street": "ул. Гродненская",
            "registeredaddress-0-house_number": "20к3",
            "registeredaddress-0-office_number": 1,

            "bankbranchaddress-TOTAL_FORMS": 1,
            "bankbranchaddress-INITIAL_FORMS": 0,
            "bankbranchaddress-MIN_NUM_FORMS": 0,
            "bankbranchaddress-MAX_NUM_FORMS": 1,
            "bankbranchaddress-0-postal_code": 220091,
            "bankbranchaddress-0-region": "Гомельская обл.",
            "bankbranchaddress-0-district": "Гомельский р-н",
            "bankbranchaddress-0-locality": "Гомель",
            "bankbranchaddress-0-street": "ул. Гомельская",
            "bankbranchaddress-0-house_number": "60/2",
            "bankbranchaddress-0-office_number": 201,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        object_added: bool = Company.objects.filter(
            name=data["name"],
            unp=data["unp"],
            IBAN=data["IBAN"],
            bank_name=data["bank_name"],
            BIC=data["BIC"]
        ).exists()
        self.assertTrue(object_added)

        object_added: bool = RegisteredAddress.objects.filter(
            locality=data["registeredaddress-0-locality"],
            street=data["registeredaddress-0-street"],
            house_number=data["registeredaddress-0-house_number"],
            office_number=data["registeredaddress-0-office_number"],
        ).exists()
        self.assertTrue(object_added)

        object_added: bool = BankBranchAddress.objects.filter(
            locality=data["bankbranchaddress-0-locality"],
            street=data["bankbranchaddress-0-street"],
            house_number=data["bankbranchaddress-0-house_number"],
            office_number=data["bankbranchaddress-0-office_number"],
        ).exists()
        self.assertTrue(object_added)

    def test_add_typeofjob(self):
        url = reverse(f"admin:{CatalogConfig.name}_typeofjobs_add")
        data = {
            "name": "test_type",
            "service_descriptions": "test service descriptions",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        object_added: bool = TypeOfJobs.objects.filter(
            name=data["name"],
            service_descriptions=data["service_descriptions"]
        ).exists()
        self.assertTrue(object_added)

    def test_add_budgetcalculation(self):
        url = reverse(f"admin:{CommerceConfig.name}_budgetcalculation_add")
        data = {
            "workload": 168,
            "hourly_rate": 5.8,
            "outsourcing_costs": 49.98,
            "profit": 25,
            "type_of_jobs": 2,
            "planned_business_trips-TOTAL_FORMS": 1,
            "planned_business_trips-INITIAL_FORMS": 0,
            "planned_business_trips-MIN_NUM_FORMS": 0,
            "planned_business_trips-MAX_NUM_FORMS": 1000,
            "planned_business_trips-0-day_count": 1,
            "planned_business_trips-0-staff_count": 2,
            "planned_business_trips-0-lodging_cost": 50,
            "planned_business_trips-0-public_transportation_fare": 50,
            "planned_business_trips-0-one_way_distance_on_company_transport": 250,
            "planned_business_trips-0-locality": "Дзержинск",
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        object_added: bool = BudgetCalculation.objects.filter(
            workload=data["workload"],
            hourly_rate=data["hourly_rate"],
            outsourcing_costs=data["outsourcing_costs"],
            profit=data["profit"],
            type_of_jobs=data["type_of_jobs"]
        ).exists()
        self.assertTrue(object_added)

        object_added: bool = PlannedBusinessTrip.objects.filter(
            day_count=data["planned_business_trips-0-day_count"],
            staff_count=data["planned_business_trips-0-staff_count"],
            lodging_cost=data["planned_business_trips-0-lodging_cost"],
            public_transportation_fare=data["planned_business_trips-0-public_transportation_fare"],
            locality=data["planned_business_trips-0-locality"],
        ).exists()
        self.assertTrue(object_added)

    def test_add_commercialproposal(self):
        url = reverse(f"admin:{CommerceConfig.name}_commercialproposal_add")
        data = {
            "service_descriptions": "Тестовое описание",
            "service_delivery_period": 60,
            "company": 114,
            "budget_calculations-TOTAL_FORMS": 0,
            "budget_calculations-INITIAL_FORMS": 0,
            "budget_calculations-MIN_NUM_FORMS": 0,
            "budget_calculations-MAX_NUM_FORMS": 1000,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        object_added: bool = CommercialProposal.objects.filter(
            service_descriptions=data["service_descriptions"],
            service_delivery_period=data["service_delivery_period"],
            company=data["company"]
        ).exists()
        self.assertTrue(object_added)

    def test_add_serviceagreement(self):
        url = reverse(f"admin:{CommerceConfig.name}_serviceagreement_add")
        data = {
            "service_descriptions": "Тестовое описание",
            "number": "тестовый номер",
            "date_of_signing": "2023-07-03",
            "act_status": "not completed",
            "commercial_proposals-TOTAL_FORMS": 0,
            "commercial_proposals-INITIAL_FORMS": 0,
            "commercial_proposals-MIN_NUM_FORMS": 0,
            "commercial_proposals-MAX_NUM_FORMS": 100,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        object_added: bool = ServiceAgreement.objects.filter(
            service_descriptions=data["service_descriptions"],
            number=data["number"],
            date_of_signing=data["date_of_signing"],
            act_status=data["act_status"],
        ).exists()
        self.assertTrue(object_added)
