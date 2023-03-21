from django.conf import settings
from django.db import models


class ActOfCompletedWork(models.Model):
    COMPLETED = "completed"
    NOT_COMPLETED = "not completed"
    STATUSES = (
        (COMPLETED, "completed"),
        (NOT_COMPLETED, "not completed"),
    )
    stage_number = models.IntegerField(null=False)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    man_hours = models.FloatField(null=False)
    status = models.CharField(max_length=20, choices=STATUSES, default=NOT_COMPLETED)
    responsible_employee = models.ForeignKey(
        "Employee", on_delete=models.CASCADE, related_name="acts_of_employee", null=True
    )
    month_of_completed = models.ForeignKey(
        "Month", on_delete=models.CASCADE, related_name="acts", null=True
    )

    month_signing_the_act = models.ForeignKey(
        "Month", on_delete=models.CASCADE, related_name="signing_acts", null=True
    )
    month_of_accounting_act_in_salary = models.ForeignKey(
        "Month", on_delete=models.CASCADE, related_name="acts_in_salary", null=True
    )
    agreement = models.ForeignKey(
        "ServiceAgreement", on_delete=models.CASCADE, related_name="acts", null=True
    )

    def __str__(self):
        return f"Эт. №{self.stage_number} дог.№{self.agreement.number}"

    class Meta:
        db_table = "act_of_completed_work"


class Company(models.Model):
    name = models.CharField(max_length=150)
    unp = models.IntegerField(null=False)

    def __str__(self):
        return str(self.name)

    class Meta:
        db_table = "company"


class Employee(models.Model):
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    patronymic = models.CharField(max_length=20)
    rate = models.FloatField(null=False)

    def __str__(self):
        return f"{self.name[0]}.{self.patronymic[0]}. {self.surname}"

    class Meta:
        db_table = "employee"


class Month(models.Model):
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    count_of_working_days = models.IntegerField(null=False)
    number_of_employees = models.FloatField(null=False)

    def __str__(self):
        return self.start_date.strftime("%b.%y")

    class Meta:
        db_table = "month"


class MonthJob(models.Model):
    man_hours = models.FloatField(null=False)
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="jobs"
    )
    month = models.ForeignKey(Month, on_delete=models.CASCADE, related_name="jobs")
    act = models.ForeignKey(
        ActOfCompletedWork, on_delete=models.CASCADE, related_name="jobs"
    )

    def __str__(self):
        return f"{self.employee} - {self.act} - {self.month}"

    class Meta:
        db_table = "month_job"


class ServiceAgreement(models.Model):
    number = models.CharField(max_length=30)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    type_of_jobs = models.ForeignKey(
        "TypeOfJobs", on_delete=models.CASCADE, related_name="agreements", null=True
    )
    company = models.ForeignKey(
        "Company", on_delete=models.CASCADE, related_name="agreements", null=True
    )

    def __str__(self):
        return f"№{self.number}"

    class Meta:
        db_table = "service_agreement"


class TypeOfJobs(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "type_of_jobs"
