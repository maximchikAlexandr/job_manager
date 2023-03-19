from django.conf import settings
from django.db import models
from djmoney.models.fields import MoneyField


class ActOfCompletedWork(models.Model):
    COMPLETED = "completed"
    NOT_COMPLETED = "not completed"
    STATUSES = (
        (COMPLETED, "completed"),
        (NOT_COMPLETED, "not completed"),
    )
    stage_number = models.IntegerField(null=False)
    amount = MoneyField(max_digits=14,
                        decimal_places=2,
                        default_currency=settings.DEFAULT_CURRENCY)
    man_hours = models.FloatField(null=False)
    status = models.CharField(max_length=20, choices=STATUSES, default=NOT_COMPLETED)
    responsible_employee = models.ForeignKey("Employee",
                                             on_delete=models.CASCADE,
                                             related_name="acts")
    month_of_completed = models.ForeignKey("Month",
                                           on_delete=models.CASCADE,
                                           related_name="acts")
    agreement = models.ForeignKey("ServiceAgreement",
                                  on_delete=models.CASCADE,
                                  related_name="acts")

    def __str__(self):
        return f"Этап №{self.stage_number} договора {self.agreement.number}"

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
        return f"{self.surname} {self.name} {self.patronymic}"

    class Meta:
        db_table = "employee"


class Month(models.Model):
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    count_of_working_days = models.IntegerField(null=False)
    number_of_employees = models.FloatField(null=False)

    def __str__(self):
        return f"{self.start_date}"

    class Meta:
        db_table = "month"


class MonthJob(models.Model):
    man_hours = models.FloatField(null=False)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="jobs")
    month = models.ForeignKey(Month, on_delete=models.CASCADE, related_name="jobs")
    act = models.ForeignKey(ActOfCompletedWork, on_delete=models.CASCADE, related_name="jobs")

    def __str__(self):
        return f"{self.employee} - {self.act} - {self.month}"

    class Meta:
        db_table = "month_job"


class ServiceAgreement(models.Model):
    number = models.CharField(max_length=30)
    amount = MoneyField(max_digits=14,
                        decimal_places=2,
                        default_currency=settings.DEFAULT_CURRENCY)
    type_of_jobs = models.ForeignKey("TypeOfJobs",
                                     on_delete=models.CASCADE,
                                     related_name="agreements")
    company = models.ForeignKey("Company",
                                on_delete=models.CASCADE,
                                related_name="agreements")

    def __str__(self):
        return f"Договор №{self.number}"

    class Meta:
        db_table = "service_agreement"


class TypeOfJobs(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "type_of_jobs"
