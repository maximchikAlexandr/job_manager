from django.contrib.admin import (ModelAdmin, StackedInline, TabularInline,
                                  models, register, widgets)
from django.core.handlers.wsgi import WSGIRequest
from job_manager_app.models import (ActOfCompletedWork, AgreementStage,
                                    BankBranchAddress, BudgetCalculation,
                                    CommercialProposal, Company, Department,
                                    Employee, HeadOfDepartment, Month,
                                    MonthJob, PlannedBusinessTrip,
                                    RegisteredAddress, ServiceAgreement,
                                    TypeOfJobs)
from job_manager_app.services import (ActOfCompletedWorkValidator,
                                      ServiceAgreementValidator)


def get_logs_by(obj, model_name):
    return models.LogEntry.objects.filter(
        object_id=obj.pk, content_type__model=model_name
    )


# ________________________________________________________________
# Catalog
@register(TypeOfJobs)
class TypeOfJobsAdmin(ModelAdmin):
    list_display = ["name"]


class RegisteredAddressInline(TabularInline):
    model = RegisteredAddress


class BankBranchAddressInline(TabularInline):
    model = BankBranchAddress


@register(Company)
class CompanyAdmin(ModelAdmin):
    inlines = [RegisteredAddressInline, BankBranchAddressInline]
    list_display = ["name"]


@register(Month)
class MonthAdmin(ModelAdmin):
    list_display = [
        "month",
        "count_of_working_days",
        "number_of_employees",
    ]
    list_editable = [
        "count_of_working_days",
        "number_of_employees",
    ]
    list_per_page = 12

    def month(self, obj):
        return obj.start_date.strftime("%b - %Y")


# ________________________________________________________________
# Commerce


class PlannedBusinessTripInline(StackedInline):
    model = PlannedBusinessTrip
    extra = 1


@register(BudgetCalculation)
class BudgetCalculationAdmin(ModelAdmin):
    list_display = ["company", "type_of_jobs", "created", "edited"]
    inlines = [PlannedBusinessTripInline]

    def company(self, obj):
        try:
            # company = obj.commercial_proposal.company
            return obj.commercial_proposal.company
        except AttributeError:
            return f"Смета не связана с КП"

    def created(self, obj=None):
        if obj is not None:
            return getattr(
                get_logs_by(obj, self.opts.model_name).first(), "action_time", None
            )
        return "unknown"

    def edited(self, obj=None):
        if obj is not None:
            return getattr(
                get_logs_by(obj, self.opts.model_name).last(), "action_time", None
            )
        return "unknown"


@register(CommercialProposal)
class CommercialProposalAdmin(ModelAdmin):
    list_display = ["service_descriptions", "created", "edited"]

    def created(self, obj=None):
        if obj is not None:
            return getattr(
                get_logs_by(obj, self.opts.model_name).first(), "action_time", None
            )
        return "unknown"

    def edited(self, obj=None):
        if obj is not None:
            return getattr(
                get_logs_by(obj, self.opts.model_name).last(), "action_time", None
            )
        return "unknown"


class StageItemInline(StackedInline):
    model = AgreementStage
    extra = 2


@register(ServiceAgreement)
class ServiceAgreementJobAdmin(ModelAdmin):
    inlines = [StageItemInline]
    list_display = ["number", "amount", "company"]
    list_editable = ["company"]

    def save_model(
        self,
        request: WSGIRequest,
        obj: ServiceAgreement,
        form: "ServiceAgreementForm",
        change: bool,
    ):
        obj.save()
        validator = ServiceAgreementValidator(obj)
        if not validator.has_valid_sum():
            validator.send_error_message(request)

    def created(self, obj=None):
        if obj is not None:
            return getattr(
                get_logs_by(obj, self.opts.model_name).first(), "action_time", None
            )
        return "unknown"

    def edited(self, obj=None):
        if obj is not None:
            return getattr(
                get_logs_by(obj, self.opts.model_name).last(), "action_time", None
            )
        return "unknown"


@register(ActOfCompletedWork)
class ActOfCompletedWorkAdmin(ModelAdmin):
    list_display = [
        "company",
        "status",
        "month_signing_the_act",
        "month_of_accounting_act_in_salary",
    ]
    list_editable = [
        "status",
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

        money_validator = ServiceAgreementValidator(obj.agreement)
        if not money_validator.has_valid_sum():
            money_validator.send_error_message(request)

        hour_validator = ActOfCompletedWorkValidator(obj)
        if not hour_validator.has_valid_sum():
            hour_validator.send_error_message(request)

    def created(self, obj=None):
        if obj is not None:
            return getattr(
                get_logs_by(obj, self.opts.model_name).first(), "action_time", None
            )
        return "unknown"

    def edited(self, obj=None):
        if obj is not None:
            return getattr(
                get_logs_by(obj, self.opts.model_name).last(), "action_time", None
            )
        return "unknown"


@register(MonthJob)
class MonthJobAdmin(ModelAdmin):
    list_display = ["company", "man_hours", "employee", "month"]
    list_editable = ["man_hours", "employee", "month"]

    def company(self, obj):
        return obj.act.agreement.company

    def save_model(
        self,
        request: WSGIRequest,
        obj: MonthJob,
        form: "MonthJobAdminWorkForm",
        change: bool,
    ):
        obj.save()

        hour_validator = ActOfCompletedWorkValidator(obj.act)
        if not hour_validator.has_valid_sum():
            hour_validator.send_error_message(request)


@register(Employee)
class EmployeeAdmin(ModelAdmin):
    list_display = ["surname", "name", "patronymic", "rate"]
    list_editable = ["rate"]


@register(Department)
class DepartmentAdmin(ModelAdmin):
    list_display = ["name", "head"]


@register(HeadOfDepartment)
class DHeadOfDepartmentAdmin(ModelAdmin):
    list_display = ["employee"]
