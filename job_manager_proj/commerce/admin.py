from django.contrib.admin import (
    ModelAdmin,
    StackedInline,
    models,
    register,
)


from commerce.models import (
    ActOfCompletedWork,
    AgreementStage,
    BudgetCalculation,
    CommercialProposal,
    PlannedBusinessTrip,
    ServiceAgreement,
)
from shared_classes import AbstractModelAdmin


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
