from django.contrib.admin import (
    ModelAdmin,
    register,
    TabularInline,
)
from django.db.models import Sum
from import_export.admin import ImportExportMixin

from commerce.models import BudgetCalculation, ServiceAgreement
from management.forms import ServiceAgreementProxyForm, MonthProxyForm
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
    extra = 0


@register(ServiceAgreementProxy)
class ServiceAgreementProxyAdmin(ReadOnlyModelMixin, ModelAdmin):
    inlines = (MonthJobTabularInline,)
    form = ServiceAgreementProxyForm
    list_per_page = 30
    readonly_fields = ("service_descriptions", "amount")
    ordering = ("-date_of_signing",)
    exclude = (
        "task_id",
        "is_signed",
        "act_status",
        "month_signing_the_act",
        "month_of_accounting_act_in_salary",
        "date_of_signing",
        "number",
    )
    list_display = ("company", "type_of_jobs", "number", "amount", "total_workload")

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
    form = MonthProxyForm
    inlines = (MonthJobTabularInline,)
    list_display = ("month", "planned_workload", "normative_workload")
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

    def month(self, obj):
        return str(obj)

    def planned_workload(self, obj):
        return MonthJob.objects.filter(month=obj).aggregate(Sum("man_hours"))[
            "man_hours__sum"
        ]

    def normative_workload(self, obj):
        return obj.count_of_working_days * 8 * obj.number_of_employees
