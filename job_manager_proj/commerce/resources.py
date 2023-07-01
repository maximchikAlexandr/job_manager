from import_export import resources

from commerce.models import (
    BudgetCalculation,
    CommercialProposal,
    ServiceAgreement,
)


class BudgetCalculationResource(resources.ModelResource):
    class Meta:
        model = BudgetCalculation


class CommercialProposalResource(resources.ModelResource):
    class Meta:
        model = CommercialProposal


class ServiceAgreementResource(resources.ModelResource):
    class Meta:
        model = ServiceAgreement
