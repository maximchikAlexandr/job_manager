from django.contrib.admin import (
    ModelAdmin,
    StackedInline,
    TabularInline,
    models,
    register,
    widgets,
)
from django import forms
from django.contrib.admin.widgets import AdminTextInputWidget

from job_manager_app.models import (
    ActOfCompletedWork,
    AgreementStage,
    BankBranchAddress,
    BudgetCalculation,
    CommercialProposal,
    Company,
    Department,
    Employee,
    HeadOfDepartment,
    Month,
    MonthJob,
    PlannedBusinessTrip,
    RegisteredAddress,
    ServiceAgreement,
    TypeOfJobs,
)


class AbstractModelAdmin(ModelAdmin):
    def get_logs_by(self, obj):
        return models.LogEntry.objects.filter(
            object_id=obj.pk, content_type__model=self.opts.model_name
        )

    def author(self, obj=None):
        if obj is not None:
            return getattr(self.get_logs_by(obj).first(), "user", None)
        return "unknown"

    def editor(self, obj=None):
        if obj is not None:
            return getattr(self.get_logs_by(obj).last(), "user", None)
        return "unknown"

    def created(self, obj=None):
        if obj is not None:
            return getattr(self.get_logs_by(obj).first(), "action_time", None)
        return "unknown"

    def edited(self, obj=None):
        if obj is not None:
            return getattr(self.get_logs_by(obj).last(), "action_time", None)
        return "unknown"


# ________________________________________________________________
# Catalog
@register(TypeOfJobs)
class TypeOfJobsAdmin(ModelAdmin):
    list_display = ["name"]


class AddressTabularInline(TabularInline):
    def formfield_for_dbfield(self, db_field, **kwargs):
        field = super().formfield_for_dbfield(db_field, **kwargs)
        if db_field.name == "postal_code":
            field.widget.attrs["style"] = "width: 100px;"
        elif db_field.name == "region":
            field.widget.attrs["style"] = "width: 150px;"
        elif db_field.name == "district":
            field.widget.attrs["style"] = "width: 150px;"
        elif db_field.name == "locality":
            field.widget.attrs["style"] = "width: 150px;"
        elif db_field.name == "street":
            field.widget.attrs["style"] = "width: 250px;"
        elif db_field.name == "house_number":
            field.widget.attrs["style"] = "width: 50px;"
        elif db_field.name == "office_number":
            field.widget.attrs["style"] = "width: 50px;"
        return field


class RegisteredAddressInline(AddressTabularInline):
    model = RegisteredAddress


class BankBranchAddressInline(AddressTabularInline):
    model = BankBranchAddress


class CompanyAdminForm(forms.ModelForm):
    name = forms.CharField(
        widget=AdminTextInputWidget(attrs={"class": "name", "style": "width: 400px;"})
    )
    unp = forms.CharField(
        widget=AdminTextInputWidget(attrs={"class": "unp", "style": "width: 260px;"})
    )

    class Meta:
        model = Company
        fields = "__all__"


@register(Company)
class CompanyAdmin(ModelAdmin):
    form = CompanyAdminForm
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
    extra = 0


@register(BudgetCalculation)
class BudgetCalculationAdmin(AbstractModelAdmin):
    list_display = ["company", "type_of_jobs", "created", "edited"]
    inlines = [PlannedBusinessTripInline]

    def company(self, obj):
        try:
            # company = obj.commercial_proposal.company
            return obj.commercial_proposal.company
        except AttributeError:
            return f"Смета не связана с КП"


@register(CommercialProposal)
class CommercialProposalAdmin(AbstractModelAdmin):
    list_display = ["company", "type_of_jobs", "created", "edited"]


class StageItemInline(StackedInline):
    model = AgreementStage
    extra = 0


@register(ServiceAgreement)
class ServiceAgreementJobAdmin(AbstractModelAdmin):
    inlines = [StageItemInline]
    list_display = ["number", "amount", "company"]

    # def save_model(
    #     self,
    #     request: WSGIRequest,
    #     obj: ServiceAgreement,
    #     form: "ServiceAgreementForm",
    #     change: bool,
    # ):
    #     obj.save()
    #     validator = ServiceAgreementValidator(obj)
    #     if not validator.has_valid_sum():
    #         validator.send_error_message(request)



@register(ActOfCompletedWork)
class ActOfCompletedWorkAdmin(AbstractModelAdmin):
    list_display = [
        "company",
        "status",
        "month_signing_the_act",
        "month_of_accounting_act_in_salary",
    ]

    def company(self, obj):
        return obj.agreement.company

    # def save_model(
    #     self,
    #     request: WSGIRequest,
    #     obj: ActOfCompletedWork,
    #     form: "ActOfCompletedWorkForm",
    #     change: bool,
    # ):
    #     obj.save()
    #
    #     money_validator = ServiceAgreementValidator(obj.agreement)
    #     if not money_validator.has_valid_sum():
    #         money_validator.send_error_message(request)
    #
    #     hour_validator = ActOfCompletedWorkValidator(obj)
    #     if not hour_validator.has_valid_sum():
    #         hour_validator.send_error_message(request)



# ________________________________________________________________
# Management
@register(MonthJob)
class MonthJobAdmin(ModelAdmin):
    list_display = ["company", "man_hours", "employee", "month"]
    list_editable = ["man_hours", "employee", "month"]

    def company(self, obj):
        return obj.act.agreement.company

    # def save_model(
    #     self,
    #     request: WSGIRequest,
    #     obj: MonthJob,
    #     form: "MonthJobAdminWorkForm",
    #     change: bool,
    # ):
    #     obj.save()
    #
    #     hour_validator = ActOfCompletedWorkValidator(obj.act)
    #     if not hour_validator.has_valid_sum():
    #         hour_validator.send_error_message(request)


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
