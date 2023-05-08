import json

from django.test import TestCase

from job_manager_app.migrations import fixtures as fixs
from job_manager_app.models import (
    ActOfCompletedWork,
    Company,
    Employee,
    Month,
    MonthJob,
    ServiceAgreement,
    TypeOfJob,
)


class UsersTestCase(TestCase):
    fixtures = fixs

    def setUp(self) -> None:
        self.valid_data = []
        for fixture in self.fixtures:
            with open(fixture, "r", encoding="utf-8") as fixture_file:
                data = json.load(fixture_file)
                self.valid_data.extend(data)

    def test_some(self):
        assert True
