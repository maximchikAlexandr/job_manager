from django.db import models

from catalog.models import Month
from commerce.models import ServiceAgreement


# ________________________________________________________________
# Management
class MonthJob(models.Model):
    PRODUCED = "produced"
    PLANNED = "planned"
    STATUSES = (
        (PRODUCED, "produced"),
        (PLANNED, "planned"),
    )
    man_hours = models.FloatField(null=False)
    employee = models.ForeignKey(
        "Employee", on_delete=models.CASCADE, related_name="jobs"
    )
    month = models.ForeignKey(Month, on_delete=models.CASCADE, related_name="jobs")
    status = models.CharField(max_length=20, choices=STATUSES, default=PLANNED)
    agreement = models.ForeignKey(
        ServiceAgreement, on_delete=models.CASCADE, related_name="jobs"
    )

    def __str__(self):
        return f"{self.employee} - {self.act} - {self.month}"



class Employee(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    patronymic = models.CharField(max_length=20)
    rate = models.FloatField(null=False)
    id_in_task_manager = models.CharField(max_length=36, null=False, blank=True)
    department = models.ForeignKey(
        "Department",
        on_delete=models.CASCADE,
        related_name="employees",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.name[0]}.{self.patronymic[0]}. {self.surname}"



class Department(models.Model):
    name = models.CharField(max_length=20)
    head = models.ForeignKey(
        "HeadOfDepartment",
        on_delete=models.CASCADE,
        related_name="departments",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name



class HeadOfDepartment(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="heads"
    )

    def __str__(self):
        return str(self.employee)


    class Meta:
        verbose_name_plural = "Heads of departments"
