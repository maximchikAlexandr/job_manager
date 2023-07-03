from django.contrib.admin import (
    ModelAdmin,
    register,
    TabularInline,
)
from import_export.admin import ImportExportMixin

from commerce.models import BudgetCalculation
from management.models import (
    Department,
    Employee,
    HeadOfDepartment,
    MonthJob,
    ServiceAgreementProxy,
    MonthProxy,
)
from management.resources import EmployeeResource
from shared_classes import ReadOnlyModelMixin


@register(MonthJob)
class MonthJobAdmin(ModelAdmin):
    list_display = ["man_hours", "employee", "month"]
    list_editable = ["employee", "month"]


@register(Employee)
class EmployeeAdmin(ImportExportMixin, ModelAdmin):
    resource_class = EmployeeResource
    list_display = ["surname", "name", "patronymic", "rate"]
    list_editable = ["rate"]


@register(Department)
class DepartmentAdmin(ModelAdmin):
    list_display = ["name", "head"]


@register(HeadOfDepartment)
class DHeadOfDepartmentAdmin(ModelAdmin):
    list_display = ["employee"]


class MonthJobTabularInline(TabularInline):
    model = MonthJob


@register(ServiceAgreementProxy)
class ServiceAgreementAdmin(ReadOnlyModelMixin, ModelAdmin):
    inlines = (MonthJobTabularInline,)
    ordering = ("-date_of_signing",)
    readonly_fields = (
        "service_descriptions",
        "amount",
    )
    exclude = (
        "task_id",
        "is_signed",
        "act_status",
        "month_signing_the_act",
        "month_of_accounting_act_in_salary",
        "date_of_signing",
        "number",
    )
    list_display = ("number", "amount", "company", "type_of_jobs", "total_workload")

    def company(self, obj):
        try:
            proposal = obj.commercial_proposals.first()
            return str(proposal.company)
        except AttributeError:
            return "Договор не связан с КП"

    def type_of_jobs(self, obj):
        budget_calculations = BudgetCalculation.objects.filter(
            commercial_proposal__service_agreement=obj
        )
        type_of_jobs = budget_calculations.values_list(
            "type_of_jobs__name", flat=True
        ).distinct()
        return "\n".join(type_of_jobs)



@register(MonthProxy)
class MonthProxyAdmin(ReadOnlyModelMixin, ModelAdmin):
    inlines = (MonthJobTabularInline,)
    readonly_fields = (
        "count_of_working_days",
        "number_of_employees",
    )
    exclude = (
        "start_date",
        "end_date",
        "patronymic",
        "year",
    )
