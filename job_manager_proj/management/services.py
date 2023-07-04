from django.db.models import Sum

from catalog.models import Month
from commerce.models import BudgetCalculation, ServiceAgreement
from management.models import MonthJob


def get_workload_by_agreement_from_calculations(agreement: ServiceAgreement) -> int:
    return BudgetCalculation.objects.filter(
        commercial_proposal__service_agreement=agreement
    ).aggregate(Sum("workload"))["workload__sum"]


def get_planned_workload_by_agreement(agreement: ServiceAgreement) -> int:
    return MonthJob.objects.filter(agreement=agreement).aggregate(Sum("man_hours"))[
        "man_hours__sum"
    ]


def get_planned_workload_by_month(month: Month) -> int:
    return MonthJob.objects.filter(month=month).aggregate(Sum("man_hours"))[
        "man_hours__sum"
    ]
