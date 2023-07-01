from commerce.forms import CommercialProposalForm, ServiceAgreementForm
from commerce.models import (
    ActOfCompletedWork,
    AgreementStage,
    BudgetCalculation,
    CommercialProposal,
    PlannedBusinessTrip,
    ServiceAgreement,
)
from django.contrib.admin import TabularInline, register
from django.core.handlers.wsgi import WSGIRequest
from shared_classes import AbstractModelAdmin


class PlannedBusinessTripInline(TabularInline):
    model = PlannedBusinessTrip
    extra = 0


@register(BudgetCalculation)
class BudgetCalculationAdmin(AbstractModelAdmin):
    list_display = ("company", "type_of_jobs", "total_cost", "created", "edited")
    readonly_fields = ("total_cost",)
    inlines = (PlannedBusinessTripInline,)
    save_on_top = True

    def company(self, obj):
        try:
            return obj.commercial_proposal.company
        except AttributeError:
            return f"Смета не связана с КП"


class BudgetCalculationInline(TabularInline):
    model = BudgetCalculation
    extra = 0
    readonly_fields = ("total_cost",)


@register(CommercialProposal)
class CommercialProposalAdmin(AbstractModelAdmin):
    inlines = (BudgetCalculationInline,)
    list_display = ("company", "job", "total_cost", "created", "edited")
    readonly_fields = ("total_cost", "type_of_jobs")
    form = CommercialProposalForm
    save_on_top = True

    def job(self, obj):
        queryset = obj.budget_calculations.all()
        types = set(str(calc.type_of_jobs) for calc in queryset)
        return "\n".join(types)

    def save_model(
        self,
        request: WSGIRequest,
        obj: CommercialProposal,
        form: "CommercialProposalForm",
        change: bool,
    ):
        super().save_model(request, obj, form, change)
        if obj.pk and not obj.type_of_jobs.exists():
            queryset = obj.budget_calculations.all()
            types = [calc.type_of_jobs for calc in queryset]
            obj.type_of_jobs.add(*types)
            super().save_model(request, obj, form, change)

        if obj.pk and obj.service_descriptions == "":
            queryset = obj.type_of_jobs.all()
            for type_ in queryset:
                obj.service_descriptions += f"{type_.service_descriptions}\n\n"
            super().save_model(request, obj, form, change)


class StageItemInline(TabularInline):
    model = AgreementStage
    extra = 0


class CommercialProposalInline(TabularInline):
    model = CommercialProposal
    extra = 0

    def has_change_permission(self, request, obj=None):
        return False


@register(ServiceAgreement)
class ServiceAgreementJobAdmin(AbstractModelAdmin):
    inlines = (StageItemInline, CommercialProposalInline)
    list_display = ("number", "amount", "company")
    readonly_fields = ("amount",)
    form = ServiceAgreementForm
    save_on_top = True


@register(ActOfCompletedWork)
class ActOfCompletedWorkAdmin(AbstractModelAdmin):
    list_display = (
        "company",
        "status",
        "month_signing_the_act",
        "month_of_accounting_act_in_salary",
    )

    def company(self, obj):
        return obj.service_agreement.company