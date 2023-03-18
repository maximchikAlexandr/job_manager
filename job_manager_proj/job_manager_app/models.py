from django.db import models
from djmoney.models.fields import MoneyField


class ActOfCompletedWork(models.Model):
    DEFAULT_CURRENCY = "BYN"
    COMPLETED = "completed"
    NOT_COMPLETED = "not completed"
    STATUSES = (
        (COMPLETED, "completed"),
        (NOT_COMPLETED, "not completed"),
    )
    id_act = models.IntegerField(primary_key=True)
    stage_number = models.IntegerField(null=False)
    amount = MoneyField(
        max_digits=14, decimal_places=2, default_currency=DEFAULT_CURRENCY
    )
    man_hours = models.FloatField(null=False)
    status = models.CharField(max_length=20, choices=STATUSES, default=NOT_COMPLETED)
    id_employee = models.ForeignKey("Employee", on_delete=models.CASCADE)
    id_month = models.ForeignKey("Month", on_delete=models.CASCADE)
    id_agreement = models.ForeignKey("ServiceAgreement", on_delete=models.CASCADE)

    class Meta:
        db_table = "act_of_completed_work"


class Company(models.Model):
    id_company = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=150)
    unp = models.IntegerField(null=False)

    class Meta:
        db_table = "company"


class Employee(models.Model):
    id_employee = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=20)
    patronymic = models.CharField(max_length=20)
    rate = models.FloatField(null=False)

    class Meta:
        db_table = "employee"


class Month(models.Model):
    id_month = models.IntegerField(primary_key=True)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)
    count_of_working_days = models.IntegerField(null=False)
    number_of_employees = models.FloatField(null=False)

    class Meta:
        db_table = "month"


class MonthJob(models.Model):
    id_job = models.IntegerField(primary_key=True)
    man_hours = models.FloatField(null=False)
    id_employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    id_month = models.ForeignKey(Month, on_delete=models.CASCADE)
    id_act = models.ForeignKey(ActOfCompletedWork, on_delete=models.CASCADE)

    class Meta:
        db_table = "month_job"


class ServiceAgreement(models.Model):
    DEFAULT_CURRENCY = "BYN"
    id_agreement = models.IntegerField(primary_key=True)
    number = models.CharField(max_length=30)
    amount = MoneyField(max_digits=14, decimal_places=2, default_currency=DEFAULT_CURRENCY)
    id_type_of_jobs = models.ForeignKey("TypeOfJobs", on_delete=models.CASCADE)
    id_company = models.ForeignKey("Company", on_delete=models.CASCADE)

    class Meta:
        db_table = "service_agreement"


class TypeOfJobs(models.Model):
    id_type_of_jobs = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=40)

    class Meta:
        db_table = "type_of_jobs"
