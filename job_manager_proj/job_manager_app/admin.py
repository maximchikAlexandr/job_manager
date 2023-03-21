from django.contrib import admin
from django.core.handlers.wsgi import WSGIRequest

from job_manager_app.models import (ActOfCompletedWork, Company, Employee,
                                    Month, MonthJob, ServiceAgreement,
                                    TypeOfJobs)
from job_manager_app.services import ServiceAgreementValidator


@admin.register(ActOfCompletedWork)
class ActOfCompletedWorkAdmin(admin.ModelAdmin):
    list_display = [
        "agreement",
        "stage_number",
        "company",
        "amount",
        "man_hours",
        "status",
        "responsible_employee",
        "month_of_completed",
        "month_signing_the_act",
        "month_of_accounting_act_in_salary",
    ]
    list_editable = [
        "man_hours",
        "status",
        "responsible_employee",
        "month_of_completed",
        "month_signing_the_act",
        "month_of_accounting_act_in_salary",
    ]

    def company(self, obj):
        return obj.agreement.company

    def save_model(
        self,
        request: WSGIRequest,
        obj: ActOfCompletedWork,
        form: "ActOfCompletedWorkForm",
        change: bool,
    ):
        obj.save()
        validator = ServiceAgreementValidator(obj.agreement)
        if not validator.validate_money():
            validator.send_error_message(request)


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
    list_display = ["act", "company", "man_hours", "employee", "month"]
    list_editable = ["man_hours", "employee", "month"]

    def company(self, obj):
        return obj.act.agreement.company


@admin.register(ServiceAgreement)
class ServiceAgreementJobAdmin(admin.ModelAdmin):
    list_display = ["number", "amount", "type_of_jobs", "company"]
    list_editable = ["type_of_jobs", "company"]

    def save_model(
        self,
        request: WSGIRequest,
        obj: ServiceAgreement,
        form: "ServiceAgreementForm",
        change: bool,
    ):
        obj.save()
        validator = ServiceAgreementValidator(obj)
        if not validator.validate_money():
            validator.send_error_message(request)


@admin.register(TypeOfJobs)
class TypeOfJobsAdmin(admin.ModelAdmin):
    list_display = ["name"]
