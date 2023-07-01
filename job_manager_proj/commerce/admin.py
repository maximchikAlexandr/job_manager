from django.contrib.admin import TabularInline, register
from django.core.handlers.wsgi import WSGIRequest
from import_export.admin import ImportExportMixin
from shared_classes import AbstractModelAdmin

from commerce.forms import CommercialProposalForm, ServiceAgreementForm
from commerce.models import (
    BudgetCalculation,
    CommercialProposal,
    PlannedBusinessTrip,
    ServiceAgreement,
)
from commerce.resources import (
    BudgetCalculationResource,
    CommercialProposalResource,
    ServiceAgreementResource,
)


class PlannedBusinessTripInline(TabularInline):
    model = PlannedBusinessTrip
    extra = 0


@register(BudgetCalculation)
class BudgetCalculationAdmin(ImportExportMixin, AbstractModelAdmin):
    resource_class = BudgetCalculationResource
    list_display = ("company", "type_of_jobs", "total_cost", "created", "edited")
    readonly_fields = ("total_cost",)
    inlines = (PlannedBusinessTripInline,)
    save_on_top = True
    list_per_page = 15
    search_fields = ("type_of_jobs__name",)

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
class CommercialProposalAdmin(ImportExportMixin, AbstractModelAdmin):
    resource_class = CommercialProposalResource
    inlines = (BudgetCalculationInline,)
    list_display = ("company", "type_of_jobs", "total_cost", "created", "edited")
    readonly_fields = ("total_cost",)
    form = CommercialProposalForm
    save_on_top = True
    list_per_page = 15
    search_fields = ("company__name",)
    exclude = ("crm_deal_id",)

    def type_of_jobs(self, obj):
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

        if obj.pk and obj.service_descriptions == "":
            queryset = obj.budget_calculations.all()
            for calc in queryset:
                obj.service_descriptions += (
                    f"{calc.type_of_jobs.service_descriptions}\n\n"
                )
            super().save_model(request, obj, form, change)


class CommercialProposalInline(TabularInline):
    model = CommercialProposal
    extra = 0

    def has_change_permission(self, request, obj=None):
        return False


@register(ServiceAgreement)
class ServiceAgreementJobAdmin(ImportExportMixin, AbstractModelAdmin):
    resource_class = ServiceAgreementResource
    inlines = (CommercialProposalInline,)
    list_display = ("number", "company", "amount", "created", "edited")
    readonly_fields = ("amount",)
    form = ServiceAgreementForm
    save_on_top = True
    list_per_page = 15
    ordering = ("-date_of_signing",)
    exclude = ("task_id",)

    def company(self, obj):
        try:
            proposal = obj.commercial_proposals.first()
            return str(proposal.company)
        except AttributeError:
            return f"Договор не связан с КП"
