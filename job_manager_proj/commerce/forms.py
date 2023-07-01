from django import forms
from django.db.models import Q

from commerce.models import (
    BudgetCalculation,
    CommercialProposal,
    ServiceAgreement,
)


class CommercialProposalForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        queryset = BudgetCalculation.objects.exclude(
            Q(commercial_proposal__isnull=False)
        )
        self.fields['new_budget_calculations'].queryset = queryset

        if not queryset.exists():
            self.fields['new_budget_calculations'].widget = forms.HiddenInput()

    new_budget_calculations = forms.ModelMultipleChoiceField(
        queryset=BudgetCalculation.objects.none(),
        required=False,
    )

    class Meta:
        model = CommercialProposal
        fields = "__all__"

    def save(self, commit=True):
        commercial_proposal = super().save(commit=commit)
        commercial_proposal.save()

        for calculation in self.cleaned_data["new_budget_calculations"].all():
            calculation.commercial_proposal = commercial_proposal
            calculation.save()

        return commercial_proposal


class ServiceAgreementForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        queryset = CommercialProposal.objects.exclude(
            Q(service_agreement__isnull=False)
        )
        self.fields['new_commercial_proposals'].queryset = queryset

        if not queryset.exists():
            self.fields['new_commercial_proposals'].widget = forms.HiddenInput()

    new_commercial_proposals = forms.ModelMultipleChoiceField(
        queryset=CommercialProposal.objects.none(),
        required=False,
    )


    class Meta:
        model = ServiceAgreement
        fields = "__all__"

    def save(self, commit=True):
        service_agreement = super().save(commit=commit)
        service_agreement.save()

        for proposal in self.cleaned_data["new_commercial_proposals"].all():
            proposal.service_agreement = service_agreement
            proposal.save()
        return service_agreement
