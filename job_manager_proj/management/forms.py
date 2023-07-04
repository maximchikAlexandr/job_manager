from django import forms

from management.models import MonthProxy, ServiceAgreementProxy
from management.services import (
    get_planned_workload_by_agreement,
    get_planned_workload_by_month,
    get_workload_by_agreement_from_calculations,
)


class ServiceAgreementProxyForm(forms.ModelForm):
    workload_in_agreement = forms.CharField(disabled=True)
    planned_workload = forms.CharField(disabled=True, required=False)

    class Meta:
        model = ServiceAgreementProxy
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, "instance", None)
        if instance and instance.pk:
            self.initial[
                "workload_in_agreement"
            ] = get_workload_by_agreement_from_calculations(self.instance)
            self.initial["planned_workload"] = get_planned_workload_by_agreement(
                self.instance
            )


class MonthProxyForm(forms.ModelForm):
    planned_workload = forms.CharField(disabled=True)
    normative_workload = forms.CharField(disabled=True, required=False)

    class Meta:
        model = MonthProxy
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = getattr(self, "instance", None)
        if instance and instance.pk:
            self.initial["planned_workload"] = get_planned_workload_by_month(
                self.instance
            )
            self.initial["normative_workload"] = (
                self.instance.count_of_working_days
                * 8
                * self.instance.number_of_employees
            )
