from django.contrib import admin
from job_manager_app.models import (
    ActOfCompletedWork,
    Company,
    Employee,
    Month,
    MonthJob,
    ServiceAgreement,
    TypeOfJobs,
)


@admin.register(ActOfCompletedWork)
class ActOfCompletedWorkAdmin(admin.ModelAdmin):
    list_display = [
        "agreement",
        "stage_number",
        "amount",
        "man_hours",
        "status",
        "responsible_employee",
        "month_of_completed",
    ]
    list_editable = [
        "amount",
        "man_hours",
        "status",
        "responsible_employee",
        "month_of_completed",
    ]


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ["surname", "name", "patronymic", "rate"]
    list_editable = ["rate"]


@admin.register(Month)
class MonthAdmin(admin.ModelAdmin):
    list_display = [
        "start_date",
        "end_date",
        "count_of_working_days",
        "number_of_employees",
    ]
    list_editable = [
        "count_of_working_days",
        "number_of_employees",
    ]


@admin.register(MonthJob)
class MonthJobAdmin(admin.ModelAdmin):
    list_display = ["act", "man_hours", "employee", "month"]
    list_editable = ["man_hours", "employee", "month"]


@admin.register(ServiceAgreement)
class ServiceAgreementJobAdmin(admin.ModelAdmin):
    list_display = ["number", "amount", "type_of_jobs", "company"]
    list_editable = ["amount", "type_of_jobs", "company"]


@admin.register(TypeOfJobs)
class TypeOfJobsAdmin(admin.ModelAdmin):
    list_display = ["name"]
