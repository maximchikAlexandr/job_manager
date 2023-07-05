from django.db import models

from catalog.models import Month, Employee
from commerce.models import ServiceAgreement
from management.services import get_workload_by_agreement_from_calculations


class MonthJob(models.Model):
    PRODUCED = "produced"
    PLANNED = "planned"
    STATUSES = (
        (PRODUCED, "produced"),
        (PLANNED, "planned"),
    )
    man_hours = models.FloatField(null=False)
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="jobs"
    )
    month = models.ForeignKey(Month, on_delete=models.CASCADE, related_name="jobs")
    status = models.CharField(max_length=20, choices=STATUSES, default=PLANNED)
    agreement = models.ForeignKey(
        ServiceAgreement, on_delete=models.CASCADE, related_name="jobs"
    )

    def __str__(self):
        return f"{self.employee} - {self.month}"


class MonthProxy(Month):
    class Meta:
        proxy = True
        verbose_name_plural = "MonthJobs - Months"
        verbose_name = "MonthJob - Month"


class ServiceAgreementProxy(ServiceAgreement):
    class Meta:
        proxy = True
        verbose_name_plural = "MonthJobs - Agreements"
        verbose_name = "MonthJob - Agreement"

    def __str__(self):
        return f"№{self.number} от {self.date_of_signing}"

    def total_workload(self):
        return get_workload_by_agreement_from_calculations(self)
